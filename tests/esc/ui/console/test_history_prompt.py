from unittest import TestCase

from fixtures import a
from prompt_toolkit.input import create_pipe_input


class HistoryPromptSession(TestCase):

    def test_two_argument_validator(self):
        with create_pipe_input() as inp:
            session = (
                a.history_prompt_session_builder
                .with_validator(r"(\w*)\s(.*)")
                .with_input(inp)
                .build()
            )
            inp.send_text("inspect desk\n")
            cmd, args = session.prompt("> ")
            self.assertEqual(cmd, "inspect")
            self.assertEqual(args, "desk")

