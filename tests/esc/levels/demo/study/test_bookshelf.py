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


class BookshelfTests(TestCase):

    def setUp(self):
        self.room_pack = room_pack
        self.game = (
            a.game_interactor_builder
             .with_room_pack(self.room_pack)
             .build()
        )
        self.game.load_room(study.name)

    def test_room_has_bookshelf_with_aliases(self):
        room = study.creator()
        unit = room.get_child("bookshelf")
        self.assertIsInstance(unit, GameObject)
        self.assertIs(room.get_child("book shelf"), unit)

    def test_bookshelf_message(self):
        ag = self.game.interact("bookshelf", "inspect")

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.BOOKSHELF_INFO)
        self.assertEqual(ag.get_hits(), set())

        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.DONE)

    def test_bookshelf_items_hidden(self):
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("practical malware analysis", "inspect")
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("black hat python", "inspect")
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("locksport", "inspect")
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("audio engine box", "inspect")
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("iphone box", "inspect")
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("yale box", "inspect")
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("raspberry pi box", "inspect")
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("elite-c box", "inspect")

    def test_inspect_reveals_practical_malware_analysis(self):
        list(self.game.interact("bookshelf", "inspect"))
        ag = self.game.interact("practical malware analysis", "inspect")
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.PRACTICAL_MALWARE_ANALYSIS_INFO)
        self.assertEqual(ag.get_hits(), set())

    def test_inspect_reveals_black_hat_python(self):
        list(self.game.interact("bookshelf", "inspect"))
        ag = self.game.interact("black hat python", "inspect")
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.BLACK_HAT_PYTHON_INFO)
        self.assertEqual(ag.get_hits(), set())

    def test_inspect_reveals_locksport(self):
        list(self.game.interact("bookshelf", "inspect"))
        ag = self.game.interact("locksport", "inspect")
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.LOCKSPORT_INFO)
        self.assertEqual(ag.get_hits(), set())

    def test_inspect_reveals_audio_engine_box(self):
        list(self.game.interact("bookshelf", "inspect"))
        ag = self.game.interact("audio engine box", "inspect")
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.AUDIO_ENGINE_BOX_INFO)
        self.assertEqual(ag.get_hits(), set())

    def test_inspect_reveals_iphone_box(self):
        list(self.game.interact("bookshelf", "inspect"))
        ag = self.game.interact("iphone box", "inspect")
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.IPHONE_BOX_INFO)
        self.assertEqual(ag.get_hits(), set())

    def test_inspect_reveals_yale_box(self):
        list(self.game.interact("bookshelf", "inspect"))
        ag = self.game.interact("yale box", "inspect")
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.YALE_BOX_INFO)
        self.assertEqual(ag.get_hits(), set())

    def test_inspect_reveals_pi_box(self):
        list(self.game.interact("bookshelf", "inspect"))
        ag = self.game.interact("pi box", "inspect")
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.RASPBERRY_BOX_INFO)
        self.assertEqual(ag.get_hits(), set())


    def test_inspect_reveals_elite_box(self):
        list(self.game.interact("bookshelf", "inspect"))
        ag = self.game.interact("elite box", "inspect")
        result = next(ag)
        self.assertEqual(ag.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(ag.get_message(), study.const.ELITE_BOX_INFO)
        self.assertEqual(ag.get_hits(), set())
