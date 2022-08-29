from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import RoomPackBuilderInteractor, RoomPack


class RoomPackBuilderInteractorTests(TestCase):

    def test_build_room_pack(self):
        interactor = RoomPackBuilderInteractor()
        room_pack = interactor.build()
        self.assertIsInstance(room_pack, RoomPack)

    def test_can_add_room(self):
        room = a.basic_room_builder.with_name("foo").build()
        interactor = RoomPackBuilderInteractor()
        interactor.with_room(room.get_name(), lambda: room)
        room_pack = interactor.build()
        self.assertIsInstance(room_pack, RoomPack)

    def test_can_get_room_from_built_factory(self):
        room = a.basic_room_builder.with_name("foo").build()
        interactor = RoomPackBuilderInteractor()
        interactor.with_room(room.get_name(), lambda: room)
        room_pack = interactor.build()
        actual = room_pack.create_room("foo")
        self.assertIs(room, actual)

    def test_delegate_factory_get_name(self):
        factory = RoomPackBuilderInteractor._DelegateRoomFactory("foo", lambda: 1)
        self.assertEquals(factory.get_name(), "foo")

    def test_delegate_factory_calls_creator_every_time(self):
        mock = Mock()
        factory = RoomPackBuilderInteractor._DelegateRoomFactory("foo", mock)
        factory.create()
        mock.assert_called()
        mock.reset_mock()
        factory.create()
        mock.assert_called()

