from unittest import TestCase
from unittest.mock import Mock

from esc.core.exception import ActionNotFoundError, ObjectNotFoundError, PropertyNotFoundError
from esc.core.typing import Action, GameObject
from fixtures import a


class BasicGameObjectTests(TestCase):

    def test_fixtures_builder_returns_game_object(self):
        game_obj = a.basic_game_object_builder.build()
        self.assertIsInstance(game_obj, GameObject)

    def test_fixtures_builder_with(self):
        builder = a.basic_game_object_builder
        builder.with_name("fixture-name")
        builder.with_children([])
        self.assertIsInstance(builder.build(), GameObject)

    def test_fixtures_builder_returns_different_objects(self):
        obj1 = a.basic_game_object_builder.build()
        obj2 = a.basic_game_object_builder.build()
        self.assertIsNot(obj1, obj2)

    def test_get_name_returns_name(self):
        game_obj = a.basic_game_object_builder.with_name("test-name").build()
        self.assertEqual(game_obj.get_name(), "test-name")

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

    def test_list_actions(self):
        action1 = Mock(spec=Action)
        action2 = Mock(spec=Action)

        action1.get_name.return_value = "action1"
        action1.get_aliases.return_value = []
        action2.get_name.return_value = "action2"
        action2.get_aliases.return_value = []

        game_obj = a.basic_game_object_builder.build()

        game_obj.add_action(action1)
        game_obj.add_action(action2)

        self.assertListEqual(game_obj.list_actions(), ["action1", "action2"])

    def test_get_action(self):
        action1 = Mock(spec=Action)
        action1.get_name.return_value = "action1"
        action1.get_aliases.return_value = []
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

    def test_get_aliases(self):
        game_obj = (
            a.basic_game_object_builder
             .with_name("foo")
             .with_alias("bar")
             .with_alias("baz")
             .build()
        )
        self.assertListEqual(game_obj.get_aliases(), ["bar", "baz"])

    def test_get_child_by_alias(self):
        game_obj = (
            a.basic_game_object_builder
             .with_name("foo")
             .with_alias("bar")
             .with_alias("baz")
             .build()
        )
        container = (
            a.basic_game_object_builder
             .with_children([game_obj])
             .build()
        )
        result = container.get_child("bar")
        self.assertIs(result, game_obj)

    def test_del_child_by_alias(self):
        game_obj = (
            a.basic_game_object_builder
             .with_name("foo")
             .with_alias("bar")
             .with_alias("baz")
             .build()
        )
        container = (
            a.basic_game_object_builder
             .with_children([game_obj])
             .build()
        )
        container.remove_child("bar")

    def test_get_action_by_alias(self):
        action1 = Mock(spec=Action)
        action1.get_name.return_value = "action1"
        action1.get_aliases.return_value = ["a", "b"]
        game_obj = a.basic_game_object_builder.build()
        game_obj.add_action(action1)
        self.assertIs(game_obj.get_action("a"), action1)
