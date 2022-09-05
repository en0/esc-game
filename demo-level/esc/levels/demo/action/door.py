from typing import Optional, List, Dict
from esc.core import (
    Action,
    ActionApi,
    InteractionResponseGenerator,
    InformResultInteractionResponse,
    InformWinInteractionResponse,
    CompleteInteractionResponse,
)


class StudyDoorUseAction(Action):

    def __init__(self, vars: Dict) -> None:
        aliases = vars.get("DOOR_UES_ALIASES", ["use", "interact"])
        self._name = aliases[0]
        self._aliases = aliases[1:]
        self._win_message = vars["WIN_MESSAGE"]

    def get_name(self) -> str:
        return self._name

    def get_aliases(self) -> List[str]:
        return self._aliases

    def trigger(
        self,
        api: ActionApi,
        using_object: Optional[str],
    ) -> InteractionResponseGenerator:
        name = api.get_owner_name()
        is_locked = api.get_object_property(name, "locked")
        if is_locked:
            yield InformResultInteractionResponse("The door is locked.")
        else:
            yield InformWinInteractionResponse(self._win_message)
        yield CompleteInteractionResponse()
