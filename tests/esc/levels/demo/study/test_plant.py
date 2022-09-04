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


class PlantTests(TestCase):

    def setUp(self):
        self.game = (
            a.game_interactor_builder
             .with_room_pack(room_pack)
             .build()
        )
        self.game.load_room(study.name)

    def test_room_has_plant_with_aliases(self):
        room = study.creator()
        unit = room.get_child("plant")
        self.assertIsInstance(unit, GameObject)
        self.assertIs(room.get_child("house plant"), unit)

    def test_plant_message(self):
        ag = self.game.interact("plant", "inspect")

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.PLANT_INFO)
        self.assertEqual(ag.get_hits(), set())

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.DONE)
