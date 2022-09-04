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


class ComputerTests(TestCase):

    def setUp(self):
        self.game = (
            a.game_interactor_builder
             .with_room_pack(room_pack)
             .build()
        )
        self.game.load_room(study.name)

    def test_room_has_computer_with_aliases(self):
        room = study.creator()
        unit = room.get_child("computer")
        self.assertIsInstance(unit, GameObject)
        self.assertIs(room.get_child("workstation"), unit)
        self.assertIs(room.get_child("desktop"), unit)
        self.assertIs(room.get_child("system"), unit)
        self.assertIs(room.get_child("machine"), unit)

    def test_computer_use_with_aliases(self):
        computer = study.creator().get_child("computer")
        unit = computer.get_action("use")
        self.assertIs(unit, computer.get_action("interact"))

    def test_computer_message(self):
        ag = self.game.interact("computer", "inspect")

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.COMPUTER_INFO)
        self.assertEqual(ag.get_hits(), set())

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.DONE)

    def test_computer_use(self):
        ag = self.game.interact("computer", "use")

        # banner
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_hits(), {"interactive"})

        # login prompt - username
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.COLLECT_INPUT)
        self.assertEqual(ag.get_hits(), {"interactive"})
        result.inform_input(study.const.COMPUTER_USERNAME)

        # login prompt - password
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.COLLECT_INPUT)
        self.assertEqual(ag.get_hits(), {"interactive", "hidden"})
        result.inform_input(study.const.COMPUTER_PASSWORDS[0])

        # motd
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.COMPUTER_MOTD)
        self.assertEqual(ag.get_hits(), {"interactive"})

        # bash
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.COLLECT_INPUT)
        self.assertEqual(ag.get_hits(), {"interactive"})
        result.inform_input(f"send_mqtt -h 192.168.22.23 -t {study.const.MQTT_TOPIC} -m unlock -u {study.const.COMPUTER_USERNAME} -p {study.const.MQTT_PASSWORD}")

        # win message
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_WIN)
        self.assertEqual(ag.get_hits(), set())

