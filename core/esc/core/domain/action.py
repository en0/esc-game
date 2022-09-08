from typing import List, Optional

from .exception import PropertyNotFoundError
from .model import CompleteInteractionResponse, InformResultInteractionResponse
from .typing import Action, ActionApi, InteractionResponseGenerator


class InformAction(Action):

    def __init__(
        self,
        name: str,
        aliases: List[str] = None,
        property: str = None,
        default_message: str = None
    ) -> None:
        self._name = name
        self._aliases = aliases or []
        self._prop = property
        self._msg = default_message

    def get_name(self) -> str:
        return self._name

    def get_aliases(self) -> List[str]:
        return list(self._aliases)

    def trigger(
        self,
        api: ActionApi,
        using_object: Optional[str],
    ) -> InteractionResponseGenerator:
        value = self._get_message(api)
        yield InformResultInteractionResponse(value)
        yield CompleteInteractionResponse()

    def _get_message(self, api: ActionApi) -> str:
        if self._prop is None:
            return self._msg
        try:
            name = api.get_owner_name()
            return api.get_object_property(name, self._prop)
        except PropertyNotFoundError:
            return self._msg


class RevealActionDecorator(Action):
    def __init__(self, action: Action) -> None:
        self._action = action

    def get_name(self) -> str:
        return self._action.get_name()

    def get_aliases(self) -> List[str]:
        return self._action.get_aliases()

    def trigger(
        self,
        api: ActionApi,
        using_object: Optional[str],
    ) -> InteractionResponseGenerator:
        name = api.get_owner_name()
        api.reveal_all_child_objects(name)
        yield from self._action.trigger(api, using_object)

