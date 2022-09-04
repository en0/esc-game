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


class DoorTests(TestCase):

    def setUp(self):
        self.game = (
            a.game_interactor_builder
             .with_room_pack(room_pack)
             .build()
        )
        self.game.load_room(study.name)

    def test_room_has_door_with_aliases(self):
        room = study.creator()
        unit = room.get_child("door")
        self.assertIsInstance(unit, GameObject)
        self.assertIs(room.get_child("exit"), unit)

    def test_door_message(self):
        ag = self.game.interact("door", "inspect")

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.DOOR_INFO)
        self.assertEqual(ag.get_hits(), set())

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.DONE)
