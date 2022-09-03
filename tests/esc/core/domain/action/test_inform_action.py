from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import InformAction, ActionApi, GameObject, InteractionResponseType


class InformActionTests(TestCase):

    def test_get_name(self):
        action = an.inform_action_builder.with_name("action").build()
        self.assertEqual(action.get_name(), "action")

    def test_generator(self):
        mock = Mock(spec=ActionApi)
        action = an.inform_action_builder.with_message("foo bar baz").build()
        ag = action.trigger(mock)

        result = next(ag)
        self.assertEqual(result.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(result.get_message(), "foo bar baz")
        self.assertEqual(result.get_hits(), set())

        result = next(ag)
        self.assertEqual(result.get_type(), InteractionResponseType.DONE)

