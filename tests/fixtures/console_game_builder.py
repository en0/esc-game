from unittest.mock import Mock
from esc.core.typing import EscapeRoomGame, RoomPack, RoomFactory, GameObject
from esc.ui.console.game import Game
from esc.ui.console.typing import GamePrompt
from prompt_toolkit.input import Input

from .base import BuilderBase
from .basic_game_prompt_builder import BasicGamePromptBuilder
from .escape_room_game_interactor_builder import EscapeRoomGameInteractorBuilder
from .static_room_pack_builder import StaticRoomPackBuilder
from .basic_game_object_builder import BasicGameObjectBuilder
from .inform_action_builder import InformActionBuilder


class ConsoleGameBuilder(BuilderBase[Game]):

    def __init__(self):
        self._room_pack = None
        self._prompt = Mock(spec=GamePrompt)
        self._esc_game = None
        self._room = None

    def with_prompt(self, value: GamePrompt) -> "ConsoleGameBuilder":
        self._prompt = value
        return self

    def with_game(self, value: EscapeRoomGame) -> "ConsoleGameBuilder":
        self._esc_game = value
        return self

    def with_room_pack(self, value: RoomPack) -> "ConsoleGameBuilder":
        self._room_pack = value
        return self

    def with_room(self, value: GameObject) -> "ConsoleGameBuilder":
        self._room = value
        return self

    def build(self) -> Game:

        if self._room_pack is None:
            mock = Mock(spec=RoomFactory)
            mock.get_name.return_value = "unittest-room"
            mock.create.side_effect = self._create_room
            self._room_pack = (
                StaticRoomPackBuilder()
                .with_name("unittest-pack")
                .with_room_factory(mock)
            )

        if self._esc_game is None:
            self._esc_game = (
                EscapeRoomGameInteractorBuilder()
                .with_room_pack(self._room_pack)
            )

        return Game(
            room_pack=self._room_pack,
            prompt=self._prompt,
            game=self._esc_game
        )

    def _create_room(self) -> GameObject:
        if self._room:
            return self._room

        return (
            BasicGameObjectBuilder()
            .with_name("container")
            .with_children([

                (
                    BasicGameObjectBuilder()
                    .with_name("room")
                    .with_action(
                        InformActionBuilder()
                        .with_name("inspect")
                        .with_default_message("unittest-room")
                        .build()
                    )
                    .build()
                ),

                (
                    BasicGameObjectBuilder()
                    .with_name("desk")
                    .with_action(
                        InformActionBuilder()
                        .with_name("inspect")
                        .with_default_message("unittest-desk")
                        .build()
                    )
                    .build()
                ),

            ])
            .build()
        )

