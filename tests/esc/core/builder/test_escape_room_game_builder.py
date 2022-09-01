from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an
from esc.core import ConfigurationError, Receiver, RoomPack


class EscapeRoomGameBuilderTests(TestCase):

    def test_build_raises_if_missing_receiver(self):
        mock = Mock(spec=RoomPack)
        builder = an.escape_room_game_builder_builder.build()
        builder.with_room_pack(mock)
        with self.assertRaises(ConfigurationError):
            builder.build()

    def test_build_raises_if_missing_room_pack(self):
        mock = Mock(spec=Receiver)
        builder = an.escape_room_game_builder_builder.build()
        builder.with_receiver(mock)
        with self.assertRaises(ConfigurationError):
            builder.build()
