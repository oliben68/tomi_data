from tomi_base.collections import flatten
from tomi_graph.entity_class_generator import EntityClassGenerator
from tomi_graph.indexes_support import IndexesSupport
from tomi_graph.nodes.node_class import NodeBaseClass
from tomi_graph.relationships.core.direction import Direction
from tomi_graph.relationships.relationship_class import RelationshipBaseClass

from tomi_data.persistency.generators.cypher.base_commands.create_entities import CreateEntities
from tomi_data.persistency.generators.cypher.base_commands.cypher_commands import CypherCommands
from tomi_data.persistency.generators.cypher.node_commands import NodeCommands


class RelationshipCommands(CypherCommands, CreateEntities):
    entity_type = RelationshipBaseClass

    @staticmethod
    def _cypher_direction_command(direction):
        if type(direction) == str:
            try:
                direction = Direction.__members__[direction]
            except KeyError:
                return "-[{relationship}]->"

        if not type(direction) == Direction:
            return "-[{relationship}]->"

        if direction == Direction.RIGHT_TO_LEFT:
            return "<-[{relationship}]-"
        else:
            return "-[{relationship}]->"

    @staticmethod
    def _create_command(verb, variable=None, entity_type=None, **properties):
        node1_var = "n1"
        node2_var = "n2"

        node1_type_name = properties["__node_1"]["__type"]
        node2_type_name = properties["__node_1"]["__type"]

        variable = variable if variable is not None else "r"

        def get_query_fields(node_type_name, props):
            if node_type_name in EntityClassGenerator.class_registry.keys():
                node_type = EntityClassGenerator.class_registry[node1_type_name]
                keys = [key for key, value in node_type.get_properties_mapping().items() if
                        value in node_type.get_unique_constraint_fields()]
                unique_constraint_value = ":".join(
                    [node_type_name] + [str(props[key]) if props[key] is not None else "" for key in keys])
                unique_constraint_name = NodeBaseClass.serialize(
                    IndexesSupport.get_unique_constraint_name(node_type))
                
                return {unique_constraint_name: unique_constraint_value}
            return props

        match1 = NodeCommands.match_command_for_type(variable=node1_var, node_type=node1_type_name, excluded=["__type"],
                                                     **get_query_fields(node1_type_name,
                                                                        properties["__node_1"]["__object"]))
        match2 = NodeCommands.match_command_for_type(variable=node2_var, node_type=node2_type_name, excluded=["__type"],
                                                     **get_query_fields(node2_type_name,
                                                                        properties["__node_2"]["__object"]))

        generate_match_cmd = match1 + "," + match2.replace("MATCH", "")

        if entity_type is not None:
            properties["__rel_type"] = entity_type

        properties_data = {k: v for k, v in properties.items() if
                           k not in ["__direction", "__rel_type", "__node_1", "__node_2"]}
        relationship_props = CypherCommands.properties_values_map(
            **{k: v for k, v in flatten(properties_data).items() if str(v).upper() != "NONE"})

        definition = variable + (":" + str(properties["__rel_type"]) if "__rel_type" in properties.keys() else "")

        connector = RelationshipCommands._cypher_direction_command(properties["__direction"]).format(
            relationship=" ".join([definition, relationship_props]))

        create_command = "{verb} ({node1}){connector}({node2})".format(verb=verb,
                                                                       node1=node1_var,
                                                                       node2=node2_var,
                                                                       connector=connector)

        return_command = "RETURN " + ", ".join([variable, node1_var, node2_var])

        return " ".join([generate_match_cmd, create_command, return_command])

    ######
    # CreateEntities methods
    ###

    @staticmethod
    def create_command_for_type(variable=None, entity_type=None, **properties):
        return RelationshipCommands._create_command("CREATE", variable=variable, entity_type=entity_type, **properties)

    @staticmethod
    def merge_command_for_type(variable=None, entity_type=None, **properties):
        return RelationshipCommands._create_command("MERGE", variable=variable, entity_type=entity_type, **properties)

    def create_command(self, variable=None):
        create_command = RelationshipCommands.create_command_for_type(variable=variable,
                                                                      entity_type=self.entity.rel_type,
                                                                      **self.entity.toDict())
        return create_command

    def merge_command(self, variable=None):
        merge_command = RelationshipCommands.merge_command_for_type(variable=variable, entity_type=self.entity.rel_type,
                                                                    **self.entity.toDict())
        return merge_command
