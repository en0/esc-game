from typing import List

from esc.core.exception import (RoomPackNotFoundError)
from esc.core.typing import (GameObject, RoomFactory, RoomPack)


class StaticRoomPack(RoomPack):

    def __init__(self, name: str, room_factories: List[RoomFactory]) -> None:
        self._name = name
        self._room_factories = {f.get_name(): f for f in room_factories}

    def get_name(self) -> str:
        return self._name

    def list_rooms(self) -> List[str]:
        return list(self._room_factories.keys())

    def create_room(self, name: str) -> GameObject:
        try:
            factory = self._room_factories[name]
        except KeyError:
            raise RoomPackNotFoundError(name)
        else:
            return factory.create()
