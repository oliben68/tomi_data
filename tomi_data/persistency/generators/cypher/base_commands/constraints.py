from abc import ABC, abstractmethod


class Constraints(ABC):
    @staticmethod
    @abstractmethod
    def create_constraint_for_type(constraint_field, entity_type=None, variable=None):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def drop_constraint_for_type(constraint_field, entity_type=None, variable=None):
        raise NotImplementedError

    @abstractmethod
    def create_constraint(self, constraint_field, variable=None):
        raise NotImplementedError

    @abstractmethod
    def drop_constraint(self, constraint_field, variable=None):
        raise NotImplementedError
