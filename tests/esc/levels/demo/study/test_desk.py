from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.levels.demo import room_pack, study
from esc.core import (
    GameObject,
    ActionApi,
    EscapeRoomGameBuilder,
    InteractionResponseType,
    ObjectNotFoundError,
)


class DeskTests(TestCase):

    def setUp(self):
        self.room_pack = room_pack
        self.game = (
            a.game_interactor_builder
             .with_room_pack(self.room_pack)
             .build()
        )
        self.game.load_room(study.name)

    def test_room_has_desk_with_aliases(self):
        room = study.creator()
        unit = room.get_child("desk")
        self.assertIsInstance(unit, GameObject)
        self.assertIs(room.get_child("table"), unit)
        self.assertIs(room.get_child("computer desk"), unit)

    def test_desk_message(self):
        ag = self.game.interact("desk", "inspect")

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.DESK_INFO)
        self.assertEqual(ag.get_hits(), set())

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.DONE)

    def test_photo_is_hidden(self):
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("photo", "inspect")

    def test_inspect_reveals_photo(self):
        list(self.game.interact("desk", "inspect"))
        ag = self.game.interact("photo", "inspect")

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.PHOTO_INFO)
        self.assertEqual(ag.get_hits(), set())
