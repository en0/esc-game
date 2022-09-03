from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import ConfigurationError, Action


class GameObjectBuilderTests(TestCase):

    def test_requires_name(self):
        builder = a.game_object_builder_builder.build()
        with self.assertRaises(ConfigurationError):
            builder.build()

    def test_object_name(self):
        builder = a.game_object_builder_builder.build()
        builder.with_name("foo")
        go = builder.build()
        self.assertEqual(go.get_name(), "foo")

    def test_child(self):
        builder = a.game_object_builder_builder.build()
        child = a.basic_game_object_builder.with_name('child').build()
        builder.with_name("foo")
        builder.with_child(child)
        go = builder.build()
        self.assertIs(go.get_child('child'), child)

    def test_children(self):
        builder = a.game_object_builder_builder.build()
        children = [
            a.basic_game_object_builder.with_name('child1').build(),
            a.basic_game_object_builder.with_name('child2').build(),
            a.basic_game_object_builder.with_name('child3').build(),
        ]
        builder.with_name("foo")
        builder.with_children(children)
        go = builder.build()
        self.assertListEqual(go.get_children(), children)

    def test_property(self):
        builder = a.game_object_builder_builder.build()
        builder.with_name("foo")
        builder.with_property("bar", "baz")
        go = builder.build()
        self.assertEqual(go.get_property("bar"), "baz")

    def test_actions(self):
        mock = Mock(spec=Action)
        mock.get_name.return_value = 'bar'
        mock.get_aliases.return_value = []
        builder = a.game_object_builder_builder.build()
        builder.with_name("foo")
        builder.with_action(mock)
        go = builder.build()
        self.assertEqual(go.get_action("bar"), mock)

    def test_aliases(self):
        builder = a.game_object_builder_builder.build()
        builder.with_name("foo")
        builder.with_alias("bar")
        builder.with_alias("baz")
        go = builder.build()
        self.assertListEqual(go.get_aliases(), ["bar", "baz"])

    def test_with_name_returns_self(self):
        builder = a.game_object_builder_builder.build()
        self.assertIs(builder.with_name("foo"), builder)

    def test_with_children_returns_self(self):
        builder = a.game_object_builder_builder.build()
        self.assertIs(builder.with_children(["foo"]), builder)

    def test_with_child_returns_self(self):
        builder = a.game_object_builder_builder.build()
        self.assertIs(builder.with_child("foo"), builder)

    def test_with_property_returns_self(self):
        builder = a.game_object_builder_builder.build()
        self.assertIs(builder.with_property("foo", "bar"), builder)

    def test_with_action_returns_self(self):
        builder = a.game_object_builder_builder.build()
        self.assertIs(builder.with_action("foo"), builder)

    def test_with_alias(self):
        builder = a.game_object_builder_builder.build()
        self.assertIs(builder.with_alias("foo"), builder)
