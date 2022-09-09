from typing import Iterator, Set
from esc.core.typing import Interaction, GameObject, Action, InteractionResponseType
from esc.core.exception import ActionError

from .action_api_interactor import ActionApiInteractor


class ObjectInteraction(Interaction):

    class __NullUsingObject:
        def get_name(self):
            return None

    def __init__(self, room_container: GameObject) -> None:
        self._room = room_container
        self._target = None
        self._action = None
        self._using = ObjectInteraction.__NullUsingObject()
        self._gen = None
        self._current = None
        self._input = None

    def set_target(self, name: str) -> None:
        self._target = self._room.get_child(name)

    def set_action(self, name: str) -> None:
        self._action = self._target.get_action(name)

    def set_using(self, name: str) -> None:
        self._using = self._room.get_child(name)

    def __iter__(self) -> Iterator[Interaction]:
        api = ActionApiInteractor(self._room, self._target)
        self._gen = self._action.trigger(api, self._using.get_name())
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
            obj_name, act_name = self._target.get_name(), self._action.get_name()
            raise ActionError(obj_name, act_name) from ex

    def _set_current_and_send(self):
        try:
            self._current = self._gen.send(self._input)
        except StopIteration:
            raise
        except Exception as ex:
            obj_name, act_name = self._target.get_name(), self._action.get_name()
            raise ActionError(obj_name, act_name) from ex

    def inform_input(self, value: str) -> None:
        self._input = value

    def get_type(self) -> InteractionResponseType:
        return self._current.get_type()

    def get_message(self) -> str:
        return self._current.get_message()

    def get_hints(self) -> Set[str]:
        return self._current.get_hints()

