from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import Receiver, InteractiveActionReceiver


class BasicActionReceiverTests(TestCase):

    def setUp(self):
        self.receiver = Mock(spec=Receiver)
        self.thing1 = (
            a.basic_game_object_builder
             .with_name("thing1")
             .with_property("foo", "bar")
             .build()
        )
        self.thing2 = (
            a.basic_game_object_builder
             .with_name("thing2")
             .build()
        )
        self.thing2_1 = (
            a.basic_game_object_builder
             .with_name("thing2_1")
             .build()
        )
        self.thing2.add_child(self.thing2_1)
        self.room_container = (
            a.basic_game_object_builder
             .with_children([self.thing1, self.thing2])
             .build()
        )
        builder = a.basic_action_receiver_builder
        builder.with_sender(self.thing1)
        builder.with_receiver(self.receiver)
        builder.with_room(self.room_container)
        self.interactor = builder.build()

    def test_win(self):
        self.interactor.win("You Win!")
        self.receiver.inform_win.assert_called_with("You Win!")

    def test_set_property(self):
        self.interactor.set_object_property("thing2", "foo", "bar")
        self.assertEqual(self.thing2.get_property("foo"), "bar")

    def test_get_property(self):
        self.assertEqual(self.interactor.get_object_property("thing1", "foo"), "bar")

    def test_reveal_child(self):
        self.interactor.reveal_child_object("thing2", "thing2_1")
        self.assertIs(self.room_container.get_child("thing2_1"), self.thing2_1)

    def test_colllect_input(self):
        self.receiver.collect_input.return_value = "this is the response"
        result = self.interactor.collect_input("This is a prompt.", {"unittest"})
        self.receiver.collect_input.assert_called_with("thing1", "This is a prompt.", {"unittest"})
        self.assertEqual(result, "this is the response")

    def test_inform_response(self):
        self.interactor.inform_response("This is a prompt.")
        self.receiver.inform_response.assert_called_with("thing1", "This is a prompt.")

    def test_interactive_session(self):
        with self.interactor.interactive_session({"foo"}) as interactor:
            self.receiver.start_interactive_session.assert_called_with("thing1", {"foo"})
            self.assertIsInstance(interactor, InteractiveActionReceiver)
        self.receiver.end_interactive_session.assert_called_with("thing1")

    def test_interactive_session_collect_input(self):
        interactor: InteractiveActionReceiver
        with self.interactor.interactive_session({"foo"}) as interactor:
            interactor.collect_input("This is a prompt.", {"unittest"})
        self.receiver.collect_input.assert_called_with("thing1", "This is a prompt.", {"unittest"})


    def test_interactive_session_inform_response(self):
        interactor: InteractiveActionReceiver
        with self.interactor.interactive_session({"foo"}) as interactor:
            interactor.inform_response("This is a message.")
        self.receiver.inform_response.assert_called_with("thing1", "This is a message.")

    def test_get_owner_name(self):
        self.assertEqual(self.interactor.get_owner_name(), self.thing1.get_name())
