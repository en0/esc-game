from typing import Optional, List
from .exception import PropertyNotFoundError
from .typing import (
    Action,
    ActionApi,
    GameObject,
    InteractionResponseGenerator,
)
from .model import (
    CompleteInteractionResponse,
    CollectInputInteractionResponse,
    InformResultInteractionResponse,
    InformWinInteractionResponse,
)


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
        using_object: Optional[GameObject],
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

