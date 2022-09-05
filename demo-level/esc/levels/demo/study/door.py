from typing import Optional, List
from esc.core import (
    Action,
    ActionApi,
    InteractionResponseGenerator,
    InformResultInteractionResponse,
    InformWinInteractionResponse,
    CompleteInteractionResponse,
)

from . import const


class UseDoorAction(Action):

    def get_name(self) -> str:
        return const.DOOR_UES_ALIASES[0]

    def get_aliases(self) -> List[str]:
        return const.DOOR_UES_ALIASES[1:]

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
            yield InformWinInteractionResponse(const.WIN_MESSAGE)
        yield CompleteInteractionResponse()
