from .game_object_builder import BasicGameObjectBuilder
from .room_builder import BasicRoomBuilder


class _A:

    @property
    def game_object_builder(self) -> BasicGameObjectBuilder:
        return BasicGameObjectBuilder()

    @property
    def room_builder(self) -> BasicRoomBuilder:
        return BasicRoomBuilder()


class _An:
    ...

a = _A()
an = _An()

