from .action_api_interactor_builder import ActionApiInteractorBuilder
from .basic_game_object_builder import BasicGameObjectBuilder
from .escape_room_game_builder_builder import EscapeRoomGameBuilderBuilder
from .escape_room_game_interactor_builder import EscapeRoomGameInteractorBuilder
from .game_object_builder_builder import GameObjectBuilderBuidler
from .basic_game_prompt_builder import BasicGamePromptBuilder
from .inform_action_builder import InformActionBuilder
from .reveal_action_decorator_bulider import RevealActionDecoratorBuilder
from .room_pack_builder_builder import RoomPackBuilderBuilder
from .static_room_pack_builder import StaticRoomPackBuilder
from .object_interaction_builder import ObjectInteractionBuilder
from .console_game_builder import ConsoleGameBuilder


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
    def action_api_interaction_builder(self) -> ActionApiInteractorBuilder:
        return ActionApiInteractorBuilder()
    @property
    def reveal_action_decorator_builder(self) -> RevealActionDecoratorBuilder:
        return RevealActionDecoratorBuilder()

    @property
    def basic_game_prompt_builder(self) -> BasicGamePromptBuilder:
        return BasicGamePromptBuilder()

    @property
    def console_game_builder(self) -> ConsoleGameBuilder:
        return ConsoleGameBuilder()


class _An:

    @property
    def inform_action_builder(self) -> InformActionBuilder:
        return InformActionBuilder()

    @property
    def escape_room_game_builder_builder(self) -> EscapeRoomGameBuilderBuilder:
        return EscapeRoomGameBuilderBuilder()

    @property
    def object_interaction_builder(self) -> ObjectInteractionBuilder:
        return ObjectInteractionBuilder()

a = _A()
an = _An()

