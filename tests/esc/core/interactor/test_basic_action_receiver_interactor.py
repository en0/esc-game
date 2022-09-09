from unittest import TestCase

from fixtures import a


class BasicActionReceiverTests(TestCase):

    def setUp(self):
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
        builder = a.action_api_impl_builder
        builder.with_sender(self.thing1)
        builder.with_room(self.room_container)
        self.interactor = builder.build()

    def test_set_property(self):
        self.interactor.set_object_property("thing2", "foo", "bar")
        self.assertEqual(self.thing2.get_property("foo"), "bar")

    def test_get_property(self):
        self.assertEqual(self.interactor.get_object_property("thing1", "foo"), "bar")

    def test_reveal_child(self):
        self.interactor.reveal_child_object("thing2", "thing2_1")
        self.assertIs(self.room_container.get_child("thing2_1"), self.thing2_1)

    def test_reveal_child(self):
        self.interactor.reveal_all_child_objects("thing2")
        self.assertIs(self.room_container.get_child("thing2_1"), self.thing2_1)

    def test_get_owner_name(self):
        self.assertEqual(self.interactor.get_owner_name(), self.thing1.get_name())
