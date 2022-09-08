from typing import Iterator, Set

from esc.core.exception import ActionError
from esc.core.typing import Interaction, InteractionResponseGenerator, InteractionResponseType


class ActionInteractor(Interaction):

    def __init__(
            self,
            generator: InteractionResponseGenerator,
            object_name: str,
            action_name: str,
    ) -> None:
        self._gen = generator
        self._current = None
        self._object_name = object_name
        self._action_name = action_name
        self._input = None

    def __iter__(self) -> Iterator[Interaction]:
        return self

    def __next__(self) -> Interaction:
        if self._current is None:
            self._set_current()
        elif self._current.get_type() == InteractionResponseType.DONE:
            raise StopIteration()
        elif self._current.get_type() == InteractionResponseType.COLLECT_INPUT:
            self._set_current_and_send()
        else:
            self._set_current()
        self._input = None
        return self

    def _set_current(self):
        try:
            self._current = next(self._gen)
        except StopIteration:
            raise
        except Exception as ex:
            raise ActionError(self._object_name, self._action_name) from ex

    def _set_current_and_send(self):
        try:
            self._current = self._gen.send(self._input)
        except StopIteration:
            raise
        except Exception as ex:
            raise ActionError(self._object_name, self._action_name) from ex

    def inform_input(self, value: str) -> None:
        self._input = value

    def get_type(self) -> InteractionResponseType:
        return self._current.get_type()

    def get_message(self) -> str:
        return self._current.get_message()

    def get_hits(self) -> Set[str]:
        return self._current.get_hits()
