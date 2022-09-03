from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an
from esc.core import ConfigurationError, RoomPack


class EscapeRoomGameBuilderTests(TestCase):

    def test_build_raises_if_missing_room_pack(self):
        builder = an.escape_room_game_builder_builder.build()
        with self.assertRaises(ConfigurationError):
            builder.build()

