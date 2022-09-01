from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import RoomPack


class RoomPackBuilderTests(TestCase):

    def test_build_room_pack(self):
        builder = a.room_pack_builder_builder.build()
        room_pack = builder.build()
        self.assertIsInstance(room_pack, RoomPack)

    def test_can_add_room(self):
        room = a.basic_game_object_builder.with_name("foo").build()
        builder = a.room_pack_builder_builder.build()
        builder.with_room_container(room.get_name(), lambda: room)
        room_pack = builder.build()
        self.assertIsInstance(room_pack, RoomPack)

    def test_can_get_room_from_built_factory(self):
        room = a.basic_game_object_builder.with_name("foo").build()
        builder = a.room_pack_builder_builder.build()
        builder.with_room_container(room.get_name(), lambda: room)
        room_pack = builder.build()
        actual = room_pack.create_room("foo")
        self.assertIs(room, actual)

    def test_creator_is_called_every_time(self):
        mock = Mock()
        builder = a.room_pack_builder_builder.build()
        builder.with_room_container("foo", mock)
        room_pack = builder.build()
        room_pack.create_room("foo")
        mock.assert_called()
        mock.reset_mock()
        room_pack.create_room("foo")
        mock.assert_called()

