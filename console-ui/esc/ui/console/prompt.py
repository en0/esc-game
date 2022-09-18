import re
from typing import List, Tuple, Iterable, Dict

from prompt_toolkit.input import Input, create_input
from prompt_toolkit.output import Output, create_output
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator
from prompt_toolkit.history import History, InMemoryHistory

from .typing import GamePrompt


class BlackHoleHistory(History):

    def load_history_strings(self) -> Iterable[str]:
        while False:
            yield

    def store_string(self, string: str) -> None:
        ...

    def append_string(self, string: str) -> None:
        ...


class ValidatedPrompt:

    def __init__(
        self,
        regex_validator: str,
        validator_error: str,
        pipeline_input: Input,
        pipeline_output: Output,
        prompt_color: str = None,
        history: History = None,
    ):
        self._re_validator = re.compile(regex_validator, re.IGNORECASE)
        self._session = PromptSession(
            history=history or InMemoryHistory(),
            validator=Validator.from_callable(self._validator, validator_error),
            input=pipeline_input,
            output=pipeline_output,
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

    def __init__(
        self,
        pipeline_input: Input = None,
        pipeline_output: Output = None,
    ):
        self._choices = None
        self._session = PromptSession(
            history=BlackHoleHistory(),
            validator=Validator.from_callable(
                self._validator,
                error_message="Please select from the list above."
            ),
            input=pipeline_input if pipeline_input else create_input(),
            output=pipeline_output if pipeline_output else create_output(),
        )

    def prompt(self, message: str, choices: List[str]):
        if len(choices) == 1:
            return choices[0]
        self._choices = choices
        print(f"\n{message}")
        print("-"*len(message))
        for i, name in enumerate(choices):
            print(f"  {i+1}. {name}")
        print("")
        return self._session.prompt("> ")

    def _validator(self, text: str) -> bool:
        return text in self._choices


class BasicGamePrompt(GamePrompt):

    _main_prompt: ValidatedPrompt
    _menu_prompt: MenuPrompt
    _default_interaction_prompt: ValidatedPrompt
    _interaction_prompts: Dict[str, ValidatedPrompt]

    def __init__(self, pipeline_input: Input = None, pipeline_output: Output = None) -> None:
        self._pipeline_input = pipeline_input if pipeline_input else create_input()
        self._pipeline_output = pipeline_output if pipeline_output else create_output()
        self.reset()

    def reset(self) -> None:

        self._main_prompt = ValidatedPrompt(
            regex_validator=r"(\w*)\s?(.*)",
            validator_error="Try help to see options",
            pipeline_input=self._pipeline_input,
            pipeline_output=self._pipeline_output,
            prompt_color="#009999")

        self._menu_prompt = MenuPrompt(
            pipeline_input=self._pipeline_input,
            pipeline_output=self._pipeline_output)

        self._default_interaction_prompt = ValidatedPrompt(
            regex_validator=r".*",
            validator_error=None,
            pipeline_input=self._pipeline_input,
            pipeline_output=self._pipeline_output,
            history=BlackHoleHistory())

        self._interaction_prompts = {}

    def prompt_for_action(self, room: str) -> Tuple[str, str]:
        a, b = self._main_prompt.prompt(f"{room}> ")
        return a.lower(), b.lower()

    def prompt_with_choices(self, message: str, choices: List[str]):
        return self._menu_prompt.prompt(message, choices)

    def prompt_for_interaction(self, message: str, object_name: str = None, hidden: bool = False) -> str:
        prompt = self._get_prompt(object_name)
        return prompt.prompt(message, hidden=hidden)

    def _get_prompt(self, object_name: str) -> ValidatedPrompt:
        if object_name is None:
            return self._default_interaction_prompt
        if object_name not in self._interaction_prompts:
            self._interaction_prompts[object_name] = ValidatedPrompt(
                regex_validator=r".*",
                validator_error=None,
                pipeline_input=self._pipeline_input,
                pipeline_output=self._pipeline_output
            )
        return self._interaction_prompts[object_name]
