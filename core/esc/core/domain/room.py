from typing import List

from .game_object import GameObject
from .exceptions import OjbectNotFound


class Room:

    def __init__(self, name: str) -> None:
        self._name = name
        self._game_objects = dict()

    def get_name(self) -> str:
        return self._name

    def get_summary(self) -> str:
        return " ".join([o.get_summary() for o in self._game_objects.values()])

    def add_game_object(self, game_object: GameObject) -> None:
        self._game_objects[game_object.get_name()] = game_object

    def list_object_names(self) -> List[str]:
        return list(self._game_objects.keys())

    def get_game_object(self, game_object_name: str) -> GameObject:
        try:
            return self._game_objects[game_object_name]
        except KeyError:
            raise OjbectNotFound(self._name)

