from unittest import TestCase
from unittest.mock import Mock

from esc.core.typing import Action, ActionApi
from fixtures import a


class RevealActionDecoratorTests(TestCase):

    def test_get_name(self):
        mock = Mock(spec=Action)
        mock.get_name.return_value = "action-name"
        action = a.reveal_action_decorator_builder.with_action(mock).build()
        self.assertEqual(action.get_name(), "action-name")

    def test_get_aliases(self):
        mock = Mock(spec=Action)
        mock.get_name.return_value = "action-name"
        mock.get_aliases.return_value = ["action-alias1", "action-alias2"]
        action = a.reveal_action_decorator_builder.with_action(mock).build()
        self.assertEqual(action.get_aliases(), ["action-alias1", "action-alias2"])

    def test_calls_reveal(self):
        api = Mock(spec=ActionApi)
        api.get_owner_name.return_value = "foo"
        mock = Mock(spec=Action)
        mock.get_name.return_value = "action-name"
        mock.get_name.return_value = "action-name"
        mock.trigger.return_value = iter([])
        action = a.reveal_action_decorator_builder.with_action(mock).build()
        list(action.trigger(api, None))
        api.reveal_all_child_objects.assert_called_with("foo")

