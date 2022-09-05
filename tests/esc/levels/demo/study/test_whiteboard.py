from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.levels.demo import DemoRoomPack, study
from esc.core import (
    GameObject,
    ActionApi,
    EscapeRoomGameBuilder,
    InteractionResponseType,
    ObjectNotFoundError,
)


class WhiteboardTests(TestCase):

    def setUp(self):
        self.game = (
            a.game_interactor_builder
             .with_room_pack(DemoRoomPack())
             .build()
        )
        self.game.load_room(study.name)

    def test_room_has_whiteboard_with_aliases(self):
        room = study.creator()
        unit = room.get_child("whiteboard")
        self.assertIsInstance(unit, GameObject)
        self.assertIs(room.get_child("white board"), unit)
        self.assertIs(room.get_child("chalk board"), unit)
        self.assertIs(room.get_child("board"), unit)

    def test_whiteboard_message(self):
        ag = self.game.interact("whiteboard", "inspect")

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.WHITEBOARD_INFO)
        self.assertEqual(ag.get_hits(), set())

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.DONE)
