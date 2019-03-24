from collections.abc import MutableSequence

from tomi_base.collections import flatten
from tomi_graph.indexes_support import IndexesSupport
from tomi_graph.nodes.node_class import NodeBaseClass

from tomi_data.persistency.generators.cypher.base_commands.constraints import Constraints
from tomi_data.persistency.generators.cypher.base_commands.create_entities import CreateEntities
from tomi_data.persistency.generators.cypher.base_commands.cypher_commands import CypherCommands
from tomi_data.persistency.generators.cypher.base_commands.indexes import Indexes
from tomi_data.persistency.generators.cypher.base_commands.search_for_entities import SearchForEntities


class NodeCommands(CypherCommands, CreateEntities, Constraints, Indexes, SearchForEntities):

    entity_type = NodeBaseClass
    excluded_properties = ["__type"]
    property_prefix = "__object."

    def __init__(self, entity):
        super().__init__(entity)

    @staticmethod
    def _create_command(verb, variable, node_type=None, **properties):
        props = {k: v for k, v in properties.items() if v is not None}
        if node_type is None:
            if "__type" in props.keys():
                if len(str(props[NodeBaseClass.serialize("type")])) > 0:
                    node_type = str(props[NodeBaseClass.serialize("type")])
                else:
                    node_type = NodeCommands.entity_type.__name__
            else:
                node_type = NodeCommands.entity_type.__name__
        variable_name = node_type[0].lower() if variable is None else str(variable)
        cypher = ("CREATE" if verb == "CREATE" else "MERGE") + "({name}:{type} {properties})"

        unique_constraint_property = [p for p in properties.keys() if
                                      p.startswith(IndexesSupport.UNIQUE_CONSTRAINT_PREFIX)]

        excluded = NodeCommands.excluded_properties + unique_constraint_property
        props = CypherCommands.properties_values_map(excluded=excluded,
                                                     property_prefix=NodeCommands.property_prefix,
                                                     **props)

        return cypher.format(name=variable_name, type=node_type, properties=props)

    ######
    # CreateEntities methods
    ###

    @staticmethod
    def create_command_for_type(variable=None, entity_type=None, **properties):
        return NodeCommands._create_command("CREATE", variable, node_type=entity_type, **flatten(properties))

    @staticmethod
    def merge_command_for_type(variable=None, entity_type=None, **properties):
        return NodeCommands._create_command("MERGE", variable, node_type=entity_type, **flatten(properties))

    def _get_unique_constraint_index(self):
        if isinstance(self.entity, IndexesSupport):
            uq_key = IndexesSupport.get_unique_constraint_name(type(self.entity))
            if uq_key in self.entity.indexes.keys():
                return uq_key, self.entity.indexes[uq_key]
        return None, None

    def _add_unique_constraint_index(self, properties):
        key, value = self._get_unique_constraint_index()
        if key is not None and value is not None:
            properties[key] = self.entity.indexes[key]
        return properties

    def create_command(self, variable=None):
        properties = self._add_unique_constraint_index(flatten(self.entity.toDict()))
        return NodeCommands.create_command_for_type(variable, entity_type=type(self.entity).__name__, **properties)

    def merge_command(self, variable=None):
        properties = self._add_unique_constraint_index(flatten(self.entity.toDict()))
        return NodeCommands.merge_command_for_type(variable, entity_type=type(self.entity).__name__, **properties)

    ######
    # SearchForEntities methods
    ###

    @staticmethod
    def match_command_for_type(node_type=None, variable=None, excluded=None, **properties):
        props = {k: v for k, v in properties.items() if v is not None}
        if node_type is None and "__type" in props.keys() and len(str(props["__type"])) > 0:
            node_type = str(props["__type"])
        if node_type is not None:
            variable_name = node_type[0].lower() if variable is None else str(variable)
        else:
            variable_name = str(variable) if variable is not None else "n"

        excluded = [] if excluded is None else excluded
        query_props = CypherCommands.properties_values_map(excluded=excluded,
                                                           property_prefix=NodeCommands.property_prefix,
                                                           **flatten(props))
        if node_type is not None:
            return "MATCH ({name}:{type} {properties})".format(name=variable_name, type=node_type,
                                                               properties=query_props)
        else:
            return "MATCH ({name} {properties})".format(name=variable_name, properties=query_props)

    @staticmethod
    def where_statement_for_type(boolean_operator=None, excluded=None, **properties):
        return "WHERE " + CypherCommands.properties_values_list(boolean_operator=boolean_operator, excluded=excluded,
                                                                **properties)

    def match_command(self, variable=None, excluded=None, node_type=None):
        excluded = list(excluded) if isinstance(excluded, MutableSequence) or type(excluded) in (set, tuple) else []
        excluded = list(set(NodeCommands.excluded_properties + excluded))
        node_type = type(self.entity).__name__ if node_type is None else str(node_type)

        key, value = self._get_unique_constraint_index()

        # if there is an unique index on the node we use it for retrieval
        if key is not None and value is not None:
            properties = {key: value}
        else:
            properties = flatten(self.entity.toDict())

        return NodeCommands.match_command_for_type(variable=variable, excluded=excluded, node_type=node_type,
                                                   **properties)

    def where_statement(self, boolean_operator=None, excluded=None):
        return NodeCommands.where_statement_for_type(boolean_operator=boolean_operator, excluded=excluded,
                                                     **flatten(self.entity.toDict()))

    ######
    # Constraints methods
    ###

    @staticmethod
    def create_constraint_for_type(constraint_field, entity_type=None, variable=None):
        variable = "n" if variable is None else str(variable)
        return "CREATE CONSTRAINT ON ({variable}:{entity_type}) ASSERT {variable}.{constraint_field} IS UNIQUE".format(
            variable=variable, entity_type=entity_type, constraint_field=constraint_field)

    @staticmethod
    def drop_constraint_for_type(constraint_field, entity_type=None, variable=None):
        variable = "n" if variable is None else str(variable)
        return "DROP CONSTRAINT ON ({variable}:{entity_type}) ASSERT {variable}.{constraint_field} IS UNIQUE".format(
            variable=variable, entity_type=entity_type, constraint_field=constraint_field)

    def create_constraint(self, constraint_field, variable=None):
        return NodeCommands.create_constraint_for_type(constraint_field, entity_type=type(self).__name__,
                                                       variable=variable)

    def drop_constraint(self, constraint_field, variable=None):
        return NodeCommands.drop_constraint_for_type(constraint_field, entity_type=type(self).__name__,
                                                     variable=variable)

    ######
    # Indexes methods
    ###

    @staticmethod
    def create_index_for_type(index_field, entity_type=None):
        return "CREATE INDEX ON :{entity_type}({index_field})".format(entity_type=entity_type, index_field=index_field)

    @staticmethod
    def drop_index_for_type(index_field, entity_type=None):
        return "DROP INDEX ON :{entity_type}({index_field})".format(entity_type=entity_type, index_field=index_field)

    def create_index(self, index_field):
        return NodeCommands.create_index_for_type(type(self.entity).__name__, index_field)

    def drop_index(self, index_field):
        return NodeCommands.drop_constraint_for_type(type(self.entity).__name__, index_field)
