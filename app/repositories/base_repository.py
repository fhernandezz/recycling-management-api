from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def get_by_id(self, entity_id):
        pass

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity) -> None:
        pass

    @abstractmethod
    def save_all(self, entities: list) -> None:
        pass
