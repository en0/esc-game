from unittest import TestCase

from fixtures import a
from prompt_toolkit.input import create_pipe_input


class BasicGamePromptTests(TestCase):

    def test_two_argument_validator(self):
        with create_pipe_input() as inp:
            session = (
                a.basic_game_prompt_builder
                .with_input(inp)
                .build()
            )
            inp.send_text("inspect desk\n")
            cmd, args = session.prompt_for_action("foo")
            self.assertEqual(cmd, "inspect")
            self.assertEqual(args, "desk")

