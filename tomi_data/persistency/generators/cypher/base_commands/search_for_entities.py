from abc import ABC, abstractmethod


class SearchForEntities(ABC):
    @staticmethod
    @abstractmethod
    def match_command_for_type(entity_type, variable=None, excluded=None, node_type=None):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def where_statement_for_type(boolean_operator=None, excluded=None, **properties):
        raise NotImplementedError

    @abstractmethod
    def match_command(self, variable=None, excluded=None, node_type=None):
        raise NotImplementedError

    @abstractmethod
    def where_statement(self, boolean_operator=None, excluded=None):
        raise NotImplementedError
