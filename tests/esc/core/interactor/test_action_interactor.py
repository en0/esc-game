from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import InteractionResponseType, InteractionResponse, ActionError
from esc.core.domain.action import (
    CollectInputInteractionResponse,
    CompleteInteractionResponse,
    InformResultInteractionResponse,
    InformWinInteractionResponse,
)


class ActionInteractorTests(TestCase):

    def setUp(self):
        self.responses = [
            InformResultInteractionResponse("Hello World"),
            CollectInputInteractionResponse("> ", {"foo"}),
            InformWinInteractionResponse("Yay!"),
            CompleteInteractionResponse()
        ]
        self.inputs = []
        self.throw = False

    def test_get_message(self):
        interaction = self._get_interaction()
        expected = [response.get_message() for response in self.responses]
        actual = [response.get_message() for response in interaction]
        self.assertListEqual(actual, expected)

    def test_get_hits(self):
        interaction = self._get_interaction()
        expected = [response.get_hits() for response in self.responses]
        actual = [response.get_hits() for response in interaction]
        self.assertListEqual(actual, expected)

    def test_get_hits(self):
        interaction = self._get_interaction()
        expected = [response.get_hits() for response in self.responses]
        actual = [response.get_hits() for response in interaction]
        self.assertListEqual(actual, expected)

    def test_get_types(self):
        interaction = self._get_interaction()
        expected = [response.get_type() for response in self.responses]
        actual = [response.get_type() for response in interaction]
        self.assertListEqual(actual, expected)

    def test_inform_input(self):
        actual = []
        for response in self._get_interaction():
            if response.get_type() == InteractionResponseType.COLLECT_INPUT:
                response.inform_input("Foo bar baz")
                actual.append("Foo bar baz")
            else:
                actual.append(None)
        self.assertListEqual(self.inputs, actual)

    def test_raises_script_errors(self):
        self.throw = True
        interaction = self._get_interaction()
        with self.assertRaises(ActionError):
            next(interaction)

    def _get_interaction(self):
        return (
            an.action_interactor_builder
              .with_generator(self._fake_interactions())
              .build()
        )

    def _fake_interactions(self):
        for response in self.responses:
            if self.throw:
                raise RuntimeError()
            elif response.get_type() == InteractionResponseType.COLLECT_INPUT:
                ans = yield response
                self.inputs.append(ans)
            else:
                self.inputs.append(None)
                yield response

