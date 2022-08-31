from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import (
    Action,
    ActionError,
    ActionReceiver,
    ActionNotFoundError,
    GameObject,
    NotInteractableError,
    ObjectNotFoundError,
    PropertyNotFoundError,
)


class BasicGameObjectTests(TestCase):

    def test_fixtures_builder_returns_game_object(self):
        game_obj = a.basic_game_object_builder.build()
        self.assertIsInstance(game_obj, GameObject)

    def test_fixtures_builder_with(self):
        builder = a.basic_game_object_builder
        builder.with_name("fixture-name")
        builder.with_summary("fixture-summary")
        builder.with_children([])
        self.assertIsInstance(builder.build(), GameObject)

    def test_fixtures_builder_returns_different_objects(self):
        obj1 = a.basic_game_object_builder.build()
        obj2 = a.basic_game_object_builder.build()
        self.assertIsNot(obj1, obj2)

    def test_get_name_returns_name(self):
        game_obj = a.basic_game_object_builder.with_name("test-name").build()
        self.assertEqual(game_obj.get_name(), "test-name")

    def test_get_summary_returns_summary(self):
        game_obj = a.basic_game_object_builder.with_summary("test-summary").build()
        self.assertEqual(game_obj.get_summary(), "test-summary")

    def test_children_can_be_none(self):
        game_obj = a.basic_game_object_builder.with_children(None).build()
        self.assertListEqual(game_obj.get_children(), [])

    def test_get_children_returns_children(self):
        children = [
            a.basic_game_object_builder.with_name("child-1").build(),
            a.basic_game_object_builder.with_name("child-2").build(),
            a.basic_game_object_builder.with_name("child-3").build(),
        ]
        game_obj = a.basic_game_object_builder.with_children(children).build()
        self.assertListEqual(game_obj.get_children(), children)

    def test_add_children(self):
        child = a.basic_game_object_builder.with_name("child-3").build()
        game_obj = a.basic_game_object_builder.build()
        game_obj.add_child(child)
        self.assertListEqual(game_obj.get_children(), [child])

    def test_get_child(self):
        children = [
            a.basic_game_object_builder.with_name("child-1").build(),
            a.basic_game_object_builder.with_name("child-2").build(),
            a.basic_game_object_builder.with_name("child-3").build(),
        ]
        game_obj = a.basic_game_object_builder.with_children(children).build()
        for child in children:
            name = child.get_name()
            self.assertIs(game_obj.get_child(name), child)

    def test_get_child_raises_not_found(self):
        game_obj = a.basic_game_object_builder.build()
        with self.assertRaises(ObjectNotFoundError):
            game_obj.get_child('no-exist')

    def test_remove_child(self):
        child = a.basic_game_object_builder.with_name("child-3").build()
        game_obj = a.basic_game_object_builder.build()
        game_obj.add_child(child)
        game_obj.remove_child('child-3')
        with self.assertRaises(ObjectNotFoundError):
            game_obj.get_child('child-3')

    def test_remove_child_raises_not_found(self):
        game_obj = a.basic_game_object_builder.build()
        with self.assertRaises(ObjectNotFoundError):
            game_obj.remove_child('no-exist')

    def test_list_action_names(self):
        action1 = Mock(spec=Action)
        action2 = Mock(spec=Action)

        action1.get_name.return_value = "action1"
        action2.get_name.return_value = "action2"

        game_obj = a.basic_game_object_builder.build()

        game_obj.add_action(action1)
        game_obj.add_action(action2)

        self.assertListEqual(game_obj.list_action_names(), ["action1", "action2"])

    def test_get_action(self):
        action1 = Mock(spec=Action)
        action1.get_name.return_value = "action1"
        game_obj = a.basic_game_object_builder.build()
        game_obj.add_action(action1)
        self.assertIs(game_obj.get_action("action1"), action1)

    def test_get_raises_action_not_found(self):
        game_obj = a.basic_game_object_builder.build()
        with self.assertRaises(ActionNotFoundError):
            game_obj.get_action("action1")

    def test_get_property(self):
        game_obj = a.basic_game_object_builder.with_properties({
            "foo": "bar",
            "baz": ["quz"]
        }).build()
        self.assertEqual(game_obj.get_property("foo"), "bar")
        self.assertListEqual(game_obj.get_property("baz"), ["quz"])

    def test_set_property(self):
        game_obj = a.basic_game_object_builder.build()
        game_obj.set_property("foo", "bar")
        self.assertEqual(game_obj.get_property("foo"), "bar")

    def test_empty_property_returns_not_found(self):
        game_obj = a.basic_game_object_builder.build()
        with self.assertRaises(PropertyNotFoundError):
            game_obj.get_property("foo")

