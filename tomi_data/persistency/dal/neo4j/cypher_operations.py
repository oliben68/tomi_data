from datetime import datetime

from tomi_base.collections import expand
from neo4j.types.graph import Node as Neo4jNode
from tomi_base.collections import flatten_lists
from tomi_graph.nodes.node_class import Node, NodeBaseClass
from tomi_graph.relationships.core.direction import Direction

from tomi_data.persistency.dal.neo4j import before_operations, after_operations
from tomi_data.persistency.dal.neo4j.cypher_operations_logic import CypherOperationsLogic
from tomi_data.persistency.dal.operation import OperationType, Operation
from tomi_data.persistency.drivers.neo4j.graph_db import NEO_INSTANCE
from tomi_data.persistency.generators.cypher.graph_commands import GraphCommands
from tomi_data.persistency.generators.cypher.node_commands import NodeCommands
from tomi_data.persistency.generators.cypher.relationship_commands import RelationshipCommands


class CypherOperations(object):
    database = NEO_INSTANCE

    @staticmethod
    def _execute(transaction):
        def run_transaction(tran, command):
            result = tran.run(command)
            return result

        results = []

        with CypherOperations.database.driver.session() as session:
            for operation in transaction:
                try:
                    cypher_transaction = session.write_transaction if operation.operation != OperationType.RETRIEVE \
                        else session.read_transaction
                    results.append(cypher_transaction(run_transaction, operation.command))
                except Exception as ex:
                    operation.data = ex
                    results.append(ex)
                CypherOperations.database.operations[datetime.utcnow().timestamp()] = operation

        return results

    @staticmethod
    @after_operations(CypherOperationsLogic.guarantee_unique_constraint_created)
    @after_operations(CypherOperationsLogic.guarantee_indexes_created)
    def create_node(node, variable=None):
        return CypherOperations._execute([Operation(OperationType.CREATE,
                                                    command=NodeCommands(node).create_command(variable=variable))])

    @staticmethod
    @after_operations(CypherOperationsLogic.guarantee_unique_constraint_created)
    @after_operations(CypherOperationsLogic.guarantee_indexes_created)
    def merge_node(node, variable=None):
        return CypherOperations._execute([Operation(OperationType.CREATE,
                                                    command=NodeCommands(node).merge_command(variable=variable))])

    @staticmethod
    def query_node(node_type=None, variable=None, **properties):
        results = []
        variable = str(variable) if variable is not None else "n"
        cypher_command = "{match} RETURN {variable}".format(
            match=NodeCommands.match_command_for_type(variable=variable, node_type=node_type, **properties),
            variable=variable)

        cypher_results = CypherOperations._execute([Operation(OperationType.RETRIEVE, command=cypher_command)])

        results_data = [row for sub_results in [result.data() for result in cypher_results] for row in sub_results]

        if len(results_data) == 0:
            return results

        for data in results_data:
            result_value = data[variable]

            if type(result_value) != Neo4jNode:
                continue  # maybe raise exception here

            node_properties = {Node.get_properties_mapping()[k]: v for k, v in expand(result_value).items()}

            results.append(Node(**node_properties))

        return results

    @staticmethod
    def node_exist(node, variable=None):
        variable = str(variable) if variable is not None else "n"

        cypher_command = "{match} RETURN {variable}".format(
            match=NodeCommands(node).match_command(variable=variable, node_type=node.node_type), variable=variable)

        results = CypherOperations._execute([Operation(OperationType.RETRIEVE, command=cypher_command)])

        results_data = [row for sub_results in [result.data() for result in results] for row in sub_results]

        if len(results_data) == 0:
            return None

        result_value = results_data[0][variable]

        if type(result_value) != Neo4jNode:
            return None  # maybe raise exception here

        node_properties = {Node.get_properties_mapping()[k]: v for k, v in expand(result_value).items()}
        node_properties["node_type"] = node.node_type

        return Node(**node_properties) == node

    @staticmethod
    def query_relationship(variable=None, **properties):
        pass

    @staticmethod
    def get_relationship(node, variable=None):
        pass

    @staticmethod
    @before_operations(CypherOperationsLogic.guarantee_nodes_exist)
    def create_relationship(relationship, variable=None):
        return CypherOperations._execute([Operation(OperationType.CREATE,
                                                    command=RelationshipCommands(relationship).create_command(
                                                        variable=variable))])

    @staticmethod
    def create_nodes_relationship(node1, node2, direction=None, variable=None, rel_type=None, **properties):
        if type(direction) != Direction:
            relationship = node1 > node2
        else:
            if direction == Direction.RIGHT_TO_LEFT:
                relationship = node1 < node2
            else:
                relationship = node1 > node2

        if rel_type is not None:
            relationship = relationship.__(rel_type=str(rel_type))
        if len(properties) > 0:
            relationship = relationship.__(data=properties)

        return CypherOperations.create_relationship(relationship, variable=variable)

    @staticmethod
    def delete_all():
        return CypherOperations._execute(Operation.create(OperationType.DELETE, commands=GraphCommands.delete_all()))

    @staticmethod
    def save_graph(graph):
        results = []

        # listing all the nodes in the graph
        for node in graph.nodes.values():
            results.append(CypherOperations.create_node(node))

        # listing all the relationships in the graph
        for relationship in graph.relationships:
            results.append(CypherOperations.create_relationship(relationship))

        return results

    @staticmethod
    def create_constraint(node, constraint_field, variable=None):
        return CypherOperations._execute([Operation(OperationType.CREATE,
                                                    command=NodeCommands(node).create_constraint(constraint_field,
                                                                                                 variable=variable))])

    @staticmethod
    def create_unique_constraint(node, variable=None):
        unique_constraint_field = NodeBaseClass.serialize(node.unique_constraint_name())
        return CypherOperations._execute([Operation(OperationType.CREATE,
                                                    command=NodeCommands(node).create_constraint(
                                                        unique_constraint_field,
                                                        variable=variable))])

    @staticmethod
    def create_indexes(node, variable=None):
        results = []
        # NOTE!!!!: in neo4j composite indexes do not exist: we therefore create one index per mentioned
        # field in --ALL-- indexes
        for field in set(flatten_lists([fields for fields in node.get_type_indexes().values()])):
            results.append(CypherOperations._execute(
                [Operation(OperationType.CREATE, command=NodeCommands(node).create_index(field))]))

        return results
