from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core.typing import InteractionResponseType, InteractionResponse
from esc.core.exception import ActionError


class ObjectInteractionTests(TestCase):

    def setUp(self):
        self.examine_message = "hello, world"
        self.examine = (
            an.inform_action_builder
              .with_name("examine")
              .with_default_message(self.examine_message)
              .build()
        )
        self.desk = (
            a.basic_game_object_builder
             .with_name("desk")
             .with_action(self.examine)
             .build()
        )
        self.unit = (
            an.object_interaction_builder
              .with_game_object(self.desk)
              .build()
        )

    def test_can_interact(self):

        self.unit.set_target(self.desk.get_name())
        self.unit.set_action(self.examine.get_name())

        iter(self.unit)

        response = next(self.unit)
        self.assertEqual(response.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(response.get_message(), self.examine_message)
        self.assertEqual(response.get_hints(), set())

        response = next(self.unit)
        self.assertEqual(response.get_type(), InteractionResponseType.DONE)
        self.assertEqual(response.get_message(), None)
        self.assertEqual(response.get_hints(), set())

    def test_action_error(self):
        def _raise_error(*args, **kwargs):
            resp = Mock(spec=InteractionResponse)
            resp.get_type.return_value = InteractionResponseType.INFORM_RESULT
            resp.get_message.return_value = self.examine_message
            resp.get_hints.return_value = set()
            yield resp
            raise Exception("boom")

        self.examine.trigger = Mock(side_effect=_raise_error)

        self.unit.set_target(self.desk.get_name())
        self.unit.set_action(self.examine.get_name())

        iter(self.unit)

        response = next(self.unit)
        self.assertEqual(response.get_type(), InteractionResponseType.INFORM_RESULT)
        self.assertEqual(response.get_message(), self.examine_message)
        self.assertEqual(response.get_hints(), set())

        with self.assertRaises(ActionError):
            next(self.unit)

