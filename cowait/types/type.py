from __future__ import annotations
from abc import ABC, abstractmethod


class Type(ABC):
    """ Abstract base class for all Cowait types. """

    name: str = None

    @abstractmethod
    def validate(self, value: any, name: str) -> None:
        """ Validates a value as this type. Raises ValueError if invalid """
        raise NotImplementedError()

    def serialize(self, value: Type) -> object:
        """ Returns a JSON-serializable representation of the value """
        return value

    def deserialize(self, value: any) -> Type:
        """ Deserializes a JSON representation of a value """
        return value

    def describe(self) -> any:
        """ Creates a JSON-serializable type description for this type """
        if self.name is None:
            raise TypeError('Unnamed type')
        return self.name
