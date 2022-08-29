from typing import List, Callable
from .typing import (
    GameObject,
    RoomFactory,
    RoomPack,
    RoomCreator,
)
from .model import StaticRoomPack


class RoomPackBuilder:

    class _DelegateRoomFactory(RoomFactory):

        def __init__(self, name: str, create: RoomCreator) -> None:
            self._name = name
            self._create = create

        def get_name(self) -> str:
            return self._name

        def create(self) -> GameObject:
            return self._create()

    def __init__(self) -> None:
        self._factories = []

    def with_room(self, name: str, creator: RoomCreator) -> "RoomPackBuilder":
        factory = RoomPackBuilder._DelegateRoomFactory(name, creator)
        self._factories.append(factory)

    def build(self) -> RoomPack:
        return StaticRoomPack(self._factories)

