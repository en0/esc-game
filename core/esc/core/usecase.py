from typing import List, Callable
from .typing import (
    Game,
    Room,
    RoomFactory,
    RoomPack,
    RoomPackBuilder,
)
from .model import StaticRoomPack


class GameInteractor(Game):
    ...


class RoomPackBuilderInteractor(RoomPackBuilder):

    class _DelegateRoomFactory(RoomFactory):

        def __init__(self, name: str, create: Callable[None, Room]) -> None:
            self._name = name
            self._create = create

        def get_name(self) -> str:
            return self._name

        def create(self) -> Room:
            return self._create()

    def __init__(self) -> None:
        self._factories = []

    def with_room(self, name: str, creator: Callable[None, Room]) -> "RoomPackBuilder":
        factory = RoomPackBuilderInteractor._DelegateRoomFactory(name, creator)
        self._factories.append(factory)

    def build(self) -> RoomPack:
        return StaticRoomPack(self._factories)

