from abc import ABC, abstractmethod


class Type(ABC):
    @abstractmethod
    def validate(self, value: any, name: str) -> None:
        raise NotImplementedError()

    def serialize(self, value: any) -> 'Type':
        return value

    def deserialize(self, value: any) -> 'Type':
        return value
