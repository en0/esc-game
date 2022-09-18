from esc.ui.console.prompt import BasicGamePrompt
from prompt_toolkit.input import Input
from prompt_toolkit.output import DummyOutput, Output

from .base import BuilderBase


class BasicGamePromptBuilder(BuilderBase[BasicGamePrompt]):

    def __init__(self):
        self._input = None
        self._output = DummyOutput()

    def with_input(self, value: Input) -> "HistoryPromptSessionBuilder":
        self._input = value
        return self

    def with_output(self, value: Output) -> "HistoryPromptSessionBuilder":
        self._output = value
        return self

    def build(self) -> BasicGamePrompt:
        if self._input is None:
            raise Exception("You must specify an input")
        return BasicGamePrompt(
            pipeline_input=self._input,
            pipeline_output=self._output
        )

