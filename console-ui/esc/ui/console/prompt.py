import re
from typing import List, Tuple

from prompt_toolkit.input import Input, create_input
from prompt_toolkit.output import Output, create_output
from prompt_toolkit.shortcuts import PromptSession as PT_PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator

from .typing import PromptSession


class HistoryPromptSession(PromptSession):

    def __init__(
        self,
        re_validator: str = r".*",
        error_message: str = None,
        prompt_color: str = None,
        pipeline_input: Input = None,
        pipeline_output: Output = None,
    ):
        self._re_validator = re.compile(re_validator, re.IGNORECASE)
        self._session = PT_PromptSession(
            validator=Validator.from_callable(self._validator, error_message),
            input=(
                pipeline_input if pipeline_input
                else create_input(always_prefer_tty=True)
            ),
            output=(
                pipeline_output if pipeline_output
                else create_output(always_prefer_tty=True)
            ),
            style=(
                Style.from_dict({'prompt': prompt_color}) if prompt_color
                else Style.from_dict({})
            )
        )

    def prompt(self, message: str, hidden: bool = False) -> Tuple[str, str]:
        result = self._session.prompt(message, is_password=hidden)
        match = self._re_validator.match(result)
        if self._re_validator.groups == 0:
            return match.group(0)
        else:
            return match.groups()

    def _validator(self, text) -> bool:
        result = self._re_validator.fullmatch(text)
        if result and self._re_validator.groups == 0:
            return True
        elif result:
            # Requre first group matches
            return result.group(1) != ""
        return result is not None


class MenuPrompt:

    def __init__(self, message: str, prompt: str, choices: List[str]):
        self._message = message
        self._prompt = prompt
        self._choices = choices
        self._session = HistoryPromptSession(
            re_validator="|".join(self._choices),
            error_message="Please select from the list above."
        )

    def prompt(self):
        print(f"\n{self._message}")
        print("-"*len(self._message))
        for i, name in enumerate(self._choices):
            print(f"  {i+1}. {name}")
        print("")
        return self._session.prompt(self._prompt)
