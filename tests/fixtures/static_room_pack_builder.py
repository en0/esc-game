from typing import List
from .base import BuilderBase
from esc.core import RoomPack, RoomFactory
from esc.core.domain.model import StaticRoomPack


class StaticRoomPackBuilder(BuilderBase[RoomPack]):

    def build(self) -> RoomPack:
        return StaticRoomPack(self._room_factories)

    def with_room_factories(self, factories: List[RoomFactory]) -> "StaticRoomPackBuilder":
        for f in factories:
            self.with_room_factory(f)
        return self

    def with_room_factory(self, factory: RoomFactory) -> "StaticRoomPackBuilder":
        self._room_factories.append(factory)
        return self

    def __init__(self) -> None:
        self._room_factories = []

