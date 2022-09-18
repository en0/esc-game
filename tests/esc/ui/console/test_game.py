from contextlib import contextmanager
from esc.core.action import CompleteInteractionResponse
from esc.core.exception import ObjectNotFoundError, ActionNotFoundError
from esc.core.typing import RoomPack, EscapeRoomGame
from esc.ui.console.game import Game
from fixtures import a
from prompt_toolkit.input import create_pipe_input, Input
from typing import Tuple
from unittest import TestCase
from unittest.mock import Mock, ANY


class GameTests(TestCase):

    def setUp(self):
        self.room_pack_mock = Mock(spec=RoomPack)
        self.room_pack_mock.get_name.return_value = "unittest-pack"
        self.room_pack_mock.list_rooms.return_value = ["unittest-pack"]

        self.game_mock = Mock(spec=EscapeRoomGame)
        self.game_mock.interact.return_value = iter([CompleteInteractionResponse()])

    @contextmanager
    def console_game(self) -> Tuple[Game, Input]:
        with create_pipe_input() as inp:

            prompt = (
                a.basic_game_prompt_builder
                .with_input(inp)
                .build()
            )

            self.prompt_mock = Mock(wraps=prompt)

            yield (
                a.console_game_builder
                .with_room_pack(self.room_pack_mock)
                .with_game(self.game_mock)
                .with_prompt(self.prompt_mock)
                .build()
            ), inp

    def test_can_quit(self):
        with self.console_game() as (unit, inp):
            inp.send_text("quit\n")
            unit.play()
        self.assertEqual(self.prompt_mock.prompt_for_action.call_count, 1)

    def test_show_help(self):
        with self.console_game() as (unit, inp):
            inp.send_text("help\n")
            inp.send_text("quit\n")
            unit.play()
        self.assertEqual(self.prompt_mock.prompt_for_action.call_count, 2)

    def test_room_is_loaded(self):
        with self.console_game() as (unit, inp):
            inp.send_text("quit\n")
            unit.play()
        self.game_mock.load_room.assert_called_with("unittest-pack")

    def test_user_prompted_for_room(self):
        with self.console_game() as (unit, inp):
            inp.send_text("quit\n")
            unit.play()
        self.prompt_mock.prompt_with_choices.assert_called_with(
            message=ANY,
            choices=["unittest-pack"]
        )

    def test_room_is_inspected(self):
        with self.console_game() as (unit, inp):
            inp.send_text("quit\n")
            unit.play()
        self.game_mock.interact.assert_called_with("room", "inspect")

    def test_room_is_inspected(self):
        with self.console_game() as (unit, inp):
            inp.send_text("quit\n")
            unit.play()
        self.game_mock.interact.assert_called_with("room", "inspect")

    def test_can_interact_with_room(self):
        with self.console_game() as (unit, inp):
            inp.send_text("inspect desk\n")
            inp.send_text("quit\n")
            unit.play()
        self.game_mock.interact.assert_called_with("desk", "inspect")

