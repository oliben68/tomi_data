from abc import ABC, abstractmethod


class CreateEntities(ABC):
    @staticmethod
    @abstractmethod
    def create_command_for_type(variable=None, entity_type=None, **properties):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def merge_command_for_type(variable=None, entity_type=None, **properties):
        raise NotImplementedError

    @abstractmethod
    def create_command(self, variable=None):
        raise NotImplementedError

    @abstractmethod
    def merge_command(self, variable=None):
        raise NotImplementedError
