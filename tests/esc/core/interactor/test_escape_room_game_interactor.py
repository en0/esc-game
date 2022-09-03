from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import RoomPack


class GameInteractorTests(TestCase):

    def setUp(self):
        room_pack = self._make_room_pack()
        builder = a.game_interactor_builder
        builder.with_room_pack(room_pack)
        game = builder.build()
        self.game = game
        self.room_pack = room_pack

    def _make_room_pack(self):
        builder = a.room_pack_builder_builder.build()
        builder.with_room_container("room1", self._room1)
        builder.with_room_container("room2", self._room2)
        return builder.build()

    def _room1(self):
        room = (
            a.basic_game_object_builder
             .with_name("room")
             .build()
        )
        room.add_action(
            an.inform_action_builder
              .with_name("inspect")
              .with_message("This is a room.")
              .build()
        )
        container = (
            a.basic_game_object_builder
             .with_name("room1")
             .with_children([room])
             .build()
        )
        return container

    def _room2(self):
        chair = (
            a.basic_game_object_builder
             .with_name("chair")
             .with_action(
                 an.inform_action_builder
                   .with_name("inspect")
                   .with_message("this is a chair")
                   .build()
             )
             .with_action(
                 an.inform_action_builder
                   .with_name("foo")
                   .with_message("this is a chair")
                   .build()
             )
             .build()
        )
        desk = (
            a.basic_game_object_builder
             .with_name("desk")
             .build()
        )
        room = (
            a.basic_game_object_builder
             .with_name("room")
             .build()
        )
        container = (
            a.basic_game_object_builder
             .with_name("room2")
             .with_children([room, chair, desk])
             .build()
        )
        return container

    def test_inspect_room(self):
        self.game.load_room("room1")
        interaction = self.game.interact("room", "inspect")
        self.assertEqual(next(interaction).get_message(), "This is a room.")

    def test_get_object_actions(self):
        self.game.load_room("room2")
        result = self.game.get_object_actions()
        self.assertDictEqual(result, {
            "room": [],
            "desk": [],
            "chair": ["inspect", "foo"],
        })

