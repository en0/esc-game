from unittest import TestCase
from unittest.mock import ANY, Mock

from esc.core.exception import ObjectNotFoundError
from fixtures import a, an


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
        builder.with_name("unittest")
        builder.with_room("room1", self._room1)
        builder.with_room("room2", self._room2)
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
              .with_default_message("This is a room.")
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
                   .with_default_message("this is a chair")
                   .build()
             )
             .with_action(
                 an.inform_action_builder
                   .with_name("foo")
                   .with_default_message("this is a chair")
                   .build()
             )
             .build()
        )
        self.mock_action = Mock()
        self.mock_action.get_name.return_value = "mock"
        self.mock_action.get_aliases.return_value = []
        self.mock_action.trigger.return_value = iter([])
        desk = (
            a.basic_game_object_builder
             .with_name("desk")
             .with_action(self.mock_action)
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
            "desk": ["mock"],
            "chair": ["inspect", "foo"],
        })

    def test_using_target(self):
        self.game.load_room("room2")
        self.game.interact("desk", "mock", "room")
        self.mock_action.trigger.assert_called_with(ANY, "room")

    def test_using_target_raises_object_not_found(self):
        self.game.load_room("room2")
        with self.assertRaises(ObjectNotFoundError):
            self.game.interact("desk", "mock", "no-exist")

