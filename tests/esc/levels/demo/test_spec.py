from unittest import TestCase

from esc.levels.demo.spec import GameObjectSpec


class DemoRoomPackTests(TestCase):
    def setUp(self):
        self.spec = GameObjectSpec.from_dict({
            "name": "foo",
            "aliases": ["bar", "baz"],
            "inform_actions": [
                {
                    "message": "quz",
                    "aliases": ["quz-foo", "quz-bar"],
                    "key": "quz-baz",
                    "reveals_children": True,
                }
            ],
            "actions": ["baz-foo", "baz-bar"],
            "properties": [{"key": "bar-foo", "value": "bar-bar"}],
            "children": [{"name": "sub-foo"}],
        })

    def test_spec_from_dict(self):
        spec = self.spec
        self.assertEqual(spec.name, "foo")
        self.assertListEqual(spec.aliases, ["bar", "baz"])
        self.assertEqual(spec.inform_actions[0].message, "quz")
        self.assertListEqual(spec.inform_actions[0].aliases, ["quz-foo", "quz-bar"])
        self.assertEqual(spec.inform_actions[0].key, "quz-baz")
        self.assertTrue(spec.inform_actions[0].reveals_children)
        self.assertListEqual(spec.actions, ["baz-foo", "baz-bar"])
        self.assertEqual(spec.properties[0].key, "bar-foo")
        self.assertEqual(spec.properties[0].value, "bar-bar")
        self.assertEqual(spec.children[0].name, "sub-foo")

