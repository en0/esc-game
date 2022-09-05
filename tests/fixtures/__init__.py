from .action_interactor_builder import ActionInteractorBuilder
from .basic_action_receiver_builder import ActionReceiverInteractorBuilder
from .basic_game_object_builder import BasicGameObjectBuilder
from .escape_room_game_builder_builder import EscapeRoomGameBuilderBuilder
from .escape_room_game_interactor_builder import EscapeRoomGameInteractorBuilder
from .game_object_builder_builder import GameObjectBuilderBuidler
from .inform_action_builder import InformActionBuilder
from .reveal_action_decorator_bulider import RevealActionDecoratorBuilder
from .room_pack_builder_builder import RoomPackBuilderBuilder
from .static_room_pack_builder import StaticRoomPackBuilder
from .history_prompt_session_builder import HistoryPromptSessionBuilder


class _A:

    @property
    def basic_game_object_builder(self) -> BasicGameObjectBuilder:
        return BasicGameObjectBuilder()

    @property
    def game_object_builder_builder(self) -> GameObjectBuilderBuidler:
        return GameObjectBuilderBuidler()

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
    @property
    def reveal_action_decorator_builder(self) -> RevealActionDecoratorBuilder:
        return RevealActionDecoratorBuilder()

    @property
    def history_prompt_session_builder(self) -> HistoryPromptSessionBuilder:
        return HistoryPromptSessionBuilder()


class _An:

    @property
    def inform_action_builder(self) -> InformActionBuilder:
        return InformActionBuilder()

    @property
    def escape_room_game_builder_builder(self) -> EscapeRoomGameBuilderBuilder:
        return EscapeRoomGameBuilderBuilder()

    @property
    def action_interactor_builder(self) -> ActionInteractorBuilder:
        return ActionInteractorBuilder()

a = _A()
an = _An()

