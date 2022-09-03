from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import ActionApi, GameObject, InteractionResponseType, PropertyNotFoundError


class InformActionTests(TestCase):

    def test_get_name(self):
        action = an.inform_action_builder.with_name("action").build()
        self.assertEqual(action.get_name(), "action")

    def test_get_aliases(self):
        action = an.inform_action_builder.with_name("a").with_alias("b").build()
        self.assertListEqual(action.get_aliases(), ["b"])


    def test_property_value(self):
        api = Mock(spec=ActionApi)
        api.get_owner_name.return_value = "obj"
        api.get_object_property.return_value = "bar"
        action = (
            an.inform_action_builder
              .with_name("action")
              .with_property_key("baz")
              .with_default_message("foo")
              .build()
            )
        ag = action.trigger(api, None)
        result = next(ag)
        self.assertEqual(result.get_message(), "bar")

    def test_default_value_if_no_prop(self):
        api = Mock(spec=ActionApi)
        api.get_owner_name.return_value = "obj"
        api.get_object_property.return_value = "bla"
        action = (
            an.inform_action_builder
              .with_name("action")
              .with_default_message("foo")
              .build()
            )
        ag = action.trigger(api, None)
        result = next(ag)
        self.assertEqual(result.get_message(), "foo")

    def test_default_value(self):
        api = Mock(spec=ActionApi)
        api.get_owner_name.return_value = "obj"
        api.get_object_property.side_effect = PropertyNotFoundError("obj", "foo")
        action = (
            an.inform_action_builder
              .with_name("action")
              .with_default_message("foo")
              .build()
            )
        ag = action.trigger(api, None)
        result = next(ag)
        self.assertEqual(result.get_message(), "foo")

    def test_generator(self):
        api = Mock(spec=ActionApi)
        api.get_owner_name.return_value = "obj"
        api.get_object_property.return_value = "bar"
        action = an.inform_action_builder.with_name("a").with_property_key("b").build()
        ag = action.trigger(api, None)

        result = next(ag)
        self.assertEqual(result.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(result.get_message(), "bar")
        self.assertEqual(result.get_hits(), set())

        result = next(ag)
        self.assertEqual(result.get_type(), InteractionResponseType.DONE)

        with self.assertRaises(StopIteration):
            next(ag)

