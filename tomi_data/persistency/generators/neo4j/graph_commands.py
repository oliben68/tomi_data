from tomi_base.base.graphs.graphs.graph import Graph

from tomi_data.persistency.generators.base_generator import BaseGenerator
from tomi_data.persistency.generators.neo4j.node_commands import NodeCommands
from tomi_data.persistency.generators.neo4j.relationship_commands import RelationshipCommands


class GraphCommands(BaseGenerator):
    entity_type = Graph

    def __init__(self, entity):
        super().__init__(entity)

    def save_all(self):
        commands = [NodeCommands(node).self_generate_merge() for node in self.entity.nodes.values()] + [
            RelationshipCommands(relationship).self_generate_merge() for relationship in self.entity.relationships]
        return commands

    @staticmethod
    def delete_all():
        return ["START r=RELATIONSHIP(*) DELETE r", "MATCH(n) DELETE n"]
