from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import InformAction, ActionReceiver, GameObject


class InformActionTests(TestCase):

    def test_inform_action_informs_receiver(self):
        mock = Mock(spec=ActionReceiver)
        action = an.inform_action_builder.with_message("foo bar baz").build()
        action.trigger(mock)
        mock.inform_response.assert_called_with("foo bar baz")

    def test_get_name(self):
        action = an.inform_action_builder.with_name("action").build()
        self.assertEqual(action.get_name(), "action")

    def test_set_owner(self):
        mock_owner = Mock(spec=GameObject)
        action = an.inform_action_builder.with_name("action").build()
        action.set_owner(mock_owner)
