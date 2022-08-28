from .game_object_builder import GameObjectBuilder
from .room_builder import RoomBuilder


class _A:

    @property
    def game_object_builder(self) -> GameObjectBuilder:
        return GameObjectBuilder()

    @property
    def room_builder(self) -> RoomBuilder:
        return RoomBuilder()


class _An:
    ...

a = _A()
an = _An()

