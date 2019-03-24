from tomi_data.persistency.generators.cypher.base_commands.create_entities import CreateEntities
from tomi_data.persistency.generators.cypher.base_commands.cypher_commands import CypherCommands


class IndexCommands(CypherCommands, CreateEntities):
    ######
    # CreateEntities methods
    ###

    @staticmethod
    def create_command_for_type(variable=None, entity_type=None, **properties):
        pass

    @staticmethod
    def merge_command_for_type(variable=None, entity_type=None, **properties):
        pass

    def create_command(self, variable=None):
        pass

    def merge_command(self, variable=None):
        pass
