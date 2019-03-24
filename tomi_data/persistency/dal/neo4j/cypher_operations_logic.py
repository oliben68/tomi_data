from tomi_base.collections import flatten_lists


class CypherOperationsLogic(object):
    @staticmethod
    def guarantee_nodes_exist(*args, **kwargs):
        from tomi_data.persistency.dal.neo4j.cypher_operations import CypherOperations

        relationship = args[0]
        node1_var = "n1"
        node2_var = "n2"

        yield CypherOperations.merge_node(relationship.node_1, node1_var)
        yield CypherOperations.merge_node(relationship.node_2, node2_var)

    @staticmethod
    def guarantee_unique_constraint_created(*args, **kwargs):
        from tomi_data.persistency.dal.neo4j.cypher_operations import CypherOperations

        return CypherOperations.create_unique_constraint(args[0])

    @staticmethod
    def guarantee_indexes_created(*args, **kwargs):
        from tomi_data.persistency.dal.neo4j.cypher_operations import CypherOperations

        return CypherOperations.create_indexes(args[0])
