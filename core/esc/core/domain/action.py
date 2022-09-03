from .typing import (
    Action,
    ActionApi,
    InteractionResponseGenerator,
)
from .model import (
    CompleteInteractionResponse,
    CollectInputInteractionResponse,
    InformResultInteractionResponse,
    InformWinInteractionResponse,
)



class InformAction(Action):

    def __init__(self, name: str, message: str) -> None:
        self._name = name
        self._message = message

    def get_name(self) -> str:
        return self._name

    def trigger(
        self,
        receiver: ActionApi
    ) -> InteractionResponseGenerator:
        yield InformResultInteractionResponse(self._message)
        yield CompleteInteractionResponse()

