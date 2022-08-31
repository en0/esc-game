from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import Receiver, RoomPack, Command


class GameInteractorTests(TestCase):

    def setUp(self):
        receiver = Mock(spec=Receiver)
        room_pack = self._make_room_pack()
        builder = a.game_interactor_builder
        builder.with_receiver(receiver)
        builder.with_room_pack(room_pack)
        game = builder.build()
        self.game = game
        self.receiver = receiver
        self.room_pack = room_pack

    def _make_room_pack(self):
        builder = a.room_pack_builder_builder.build()
        builder.with_room("room1", self._room1)
        return builder.build()

    def _room1(self):
        root = a.basic_game_object_builder.with_name("root").build()
        builder = a.basic_game_object_builder
        builder.with_name("room")
        room = builder.build()
        room.add_action(
            an.inform_action_builder
              .with_name("inspect")
              .with_message("This is a room.")
              .build()
        )
        root.add_child(room)
        return root

    def test_make_action_command(self):
        self.game.load_room("room1")
        cmd = self.game.make_action_command("room", "inspect")
        self.assertIsInstance(cmd, Command)

    @skip("")
    def test_inspect_room(self):
        self.game.load_room("room1")
        self.game.make_action_command("room", "inspect").execute()
        receiver.inform_response.assert_called_with("room", "This is a room")

