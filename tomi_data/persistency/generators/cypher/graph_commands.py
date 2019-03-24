from tomi_graph.graphs.graph import Graph
from tomi_graph.nodes.node_class import NodeBaseClass

from tomi_data.persistency.generators.base_generator import BaseGenerator
from tomi_data.persistency.generators.cypher.node_commands import NodeCommands
from tomi_data.persistency.generators.cypher.relationship_commands import RelationshipCommands


class GraphCommands(BaseGenerator):
    entity_type = Graph

    def __init__(self, entity):
        super().__init__(entity)

    def save_all(self):
        commands = [NodeCommands(node).merge_command() for node in self.entity.nodes.values()] + [
            NodeCommands(node).create_constraint(NodeBaseClass.serialize(node.unique_constraint_name())) for node
            in self.entity.nodes.values()] + [RelationshipCommands(relationship).merge_command() for relationship in
                                              self.entity.relationships]
        return commands

    @staticmethod
    def delete_all():
        return ["START r=RELATIONSHIP(*) DELETE r", "MATCH(n) DELETE n"]
