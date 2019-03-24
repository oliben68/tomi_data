from abc import ABC, abstractmethod


class Indexes(ABC):
    @staticmethod
    @abstractmethod
    def create_index_for_type(index_field, entity_type=None):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def drop_index_for_type(index_field, entity_type=None):
        raise NotImplementedError

    @abstractmethod
    def create_index(self, index_field):
        raise NotImplementedError

    @abstractmethod
    def drop_index(self, index_field):
        raise NotImplementedError
