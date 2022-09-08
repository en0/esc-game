from unittest import TestCase

from esc.core.exception import ConfigurationError
from fixtures import an


class EscapeRoomGameBuilderTests(TestCase):

    def test_build_raises_if_missing_room_pack(self):
        builder = an.escape_room_game_builder_builder.build()
        with self.assertRaises(ConfigurationError):
            builder.build()

