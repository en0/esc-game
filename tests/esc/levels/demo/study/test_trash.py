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


class TrashTests(TestCase):

    def setUp(self):
        self.game = (
            a.game_interactor_builder
             .with_room_pack(DemoRoomPack())
             .build()
        )
        self.game.load_room(study.name)

    def test_room_has_trash_with_aliases(self):
        room = study.creator()
        unit = room.get_child("trash")
        self.assertIsInstance(unit, GameObject)
        self.assertIs(room.get_child("trash can"), unit)
        self.assertIs(room.get_child("waste bin"), unit)
        self.assertIs(room.get_child("trash bin"), unit)
        self.assertIs(room.get_child("waste basket"), unit)
        self.assertIs(room.get_child("waste paper basket"), unit)

    def test_trash_message(self):
        ag = self.game.interact("trash", "inspect")

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.TRASH_INFO)
        self.assertEqual(ag.get_hits(), set())

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.DONE)
