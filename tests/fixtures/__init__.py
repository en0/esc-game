from .basic_game_object_builder import BasicGameObjectBuilder
from .basic_room_builder import BasicRoomBuilder
from .delegate_command_builder import DelegateCommandBuilder
from .game_interactor_builder import GameInteractorBuilder
from .static_room_pack_builder import StaticRoomPackBuilder


class _A:

    @property
    def basic_game_object_builder(self) -> BasicGameObjectBuilder:
        return BasicGameObjectBuilder()

    @property
    def basic_room_builder(self) -> BasicRoomBuilder:
        return BasicRoomBuilder()

    @property
    def delegate_command_builder(self) -> DelegateCommandBuilder:
        return DelegateCommandBuilder()

    @property
    def game_interactor_builder(self) -> GameInteractorBuilder:
        return GameInteractorBuilder()

    @property
    def static_room_pack_builder(self) -> StaticRoomPackBuilder:
        return StaticRoomPackBuilder()


class _An:
    ...

a = _A()
an = _An()

