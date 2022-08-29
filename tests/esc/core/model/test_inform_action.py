from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import InformAction, ActionReceiver


class InformActionTests(TestCase):

    def test_inform_action_informs_receiver(self):
        mock = Mock(spec=ActionReceiver)
        action = an.inform_action_builder.with_message("foo bar baz").with_mime_type("text/plain").build()
        action.trigger(None, mock)
        mock.inform_result.assert_called_with("foo bar baz", "text/plain")

    def test_get_name(self):
        action = an.inform_action_builder.with_name("action").build()
        self.assertEqual(action.get_name(), "action")
