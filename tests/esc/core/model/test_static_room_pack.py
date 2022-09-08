from unittest import TestCase
from unittest.mock import Mock

from esc.core.exception import RoomPackNotFoundError
from esc.core.typing import GameObject, RoomFactory
from fixtures import a


class StaticRoomPackTests(TestCase):

    def test_list_room_names_returns_empty_list(self):
        room_pack = a.static_room_pack_builder.build()
        self.assertListEqual(room_pack.list_rooms(), [])

    def test_list_room_names(self):
        names = ["foo", "bar", "baz"]
        mocks = [self._mock_factory(n) for n in names]
        room_pack = a.static_room_pack_builder.with_room_factories(mocks).build()
        self.assertListEqual(room_pack.list_rooms(), names)

    def test_create_room(self):
        names = ["foo", "bar", "baz"]
        mocks = [self._mock_factory(n) for n in names]
        room_pack = a.static_room_pack_builder.with_room_factories(mocks).build()
        for name, mock in zip(names, mocks):
            self.assertIs(room_pack.create_room(name), mock.create())

    def test_create_room_raises_not_found(self):
        room_pack = a.static_room_pack_builder.build()
        with self.assertRaises(RoomPackNotFoundError):
            room_pack.create_room("no-exist")

    def test_create_room_does_not_hide_factory_exceptions(self):
        mock = self._mock_factory("foo")
        mock.create.side_effect = KeyError("OOF")
        room_pack = a.static_room_pack_builder.with_room_factory(mock).build()
        with self.assertRaises(KeyError):
            room_pack.create_room("foo")

    def _mock_factory(self, name: str, room: GameObject = None):
        mock = Mock(spec=RoomFactory)
        mock.get_name.return_value = name
        mock.create.return_value = room or Mock(spec=GameObject)
        return mock

