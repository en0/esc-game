from esc.ui.console.prompt import HistoryPromptSession
from prompt_toolkit.input import Input
from prompt_toolkit.output import DummyOutput, Output

from .base import BuilderBase


class HistoryPromptSessionBuilder(BuilderBase[HistoryPromptSession]):

    def __init__(self):
        self._re_validator = None
        self._input = None
        self._output = DummyOutput()

    def with_validator(self, value: str) -> "HistoryPromptSessionBuilder":
        self._re_validator = value
        return self

    def with_input(self, value: Input) -> "HistoryPromptSessionBuilder":
        self._input = value
        return self

    def with_output(self, value: Output) -> "HistoryPromptSessionBuilder":
        self._output = value
        return self

    def build(self) -> HistoryPromptSession:
        if self._input is None:
            raise Exception("You must specify an input")
        return HistoryPromptSession(
            re_validator=self._re_validator,
            pipeline_input=self._input,
            pipeline_output=self._output
        )

