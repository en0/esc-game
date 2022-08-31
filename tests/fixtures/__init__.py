from .basic_action_receiver_builder import ActionReceiverInteractorBuilder
from .basic_game_object_builder import BasicGameObjectBuilder
from .delegate_command_builder import DelegateCommandBuilder
from .escape_room_game_interactor_builder import EscapeRoomGameInteractorBuilder
from .inform_action_builder import InformActionBuilder
from .room_pack_builder_builder import RoomPackBuilderBuilder
from .static_room_pack_builder import StaticRoomPackBuilder


class _A:

    @property
    def basic_game_object_builder(self) -> BasicGameObjectBuilder:
        return BasicGameObjectBuilder()

    @property
    def delegate_command_builder(self) -> DelegateCommandBuilder:
        return DelegateCommandBuilder()

    @property
    def game_interactor_builder(self) -> EscapeRoomGameInteractorBuilder:
        return EscapeRoomGameInteractorBuilder()

    @property
    def static_room_pack_builder(self) -> StaticRoomPackBuilder:
        return StaticRoomPackBuilder()

    @property
    def room_pack_builder_builder(self) -> RoomPackBuilderBuilder:
        return RoomPackBuilderBuilder()

    @property
    def basic_action_receiver_builder(self) -> ActionReceiverInteractorBuilder:
        return ActionReceiverInteractorBuilder()


class _An:

    @property
    def inform_action_builder(self) -> InformActionBuilder:
        return InformActionBuilder()

a = _A()
an = _An()

