from typing import Set

from esc.core.typing import InteractionResponse, InteractionResponseType


class __InteractionBase(InteractionResponse):
    def __init__(
            self,
            interaction_type: InteractionResponseType,
            message: str,
            hints: Set[str] = None,
    ) -> None:
        self._type = interaction_type
        self._message = message
        self._hints = hints or set()

    def get_type(self) -> InteractionResponseType:
        return self._type

    def get_message(self) -> str:
        return self._message

    def get_hints(self) -> Set[str]:
        return self._hints


class CompleteInteractionResponse(__InteractionBase):
    def __init__(self) -> None:
        super().__init__(InteractionResponseType.DONE, None, None)


class CollectInputInteractionResponse(__InteractionBase):
    def __init__(self, message: str, hints: Set[str] = None) -> None:
        super().__init__(InteractionResponseType.COLLECT_INPUT, message, hints)


class InformResultInteractionResponse(__InteractionBase):
    def __init__(self, message: str, hints: Set[str] = None) -> None:
        super().__init__(InteractionResponseType.INFORM_RESULT, message, hints)


class InformWinInteractionResponse(__InteractionBase):
    def __init__(self, message: str) -> None:
        super().__init__(InteractionResponseType.INFORM_WIN, message, None)


class InformLoseInteractionResponse(__InteractionBase):
    def __init__(self, message: str) -> None:
        super().__init__(InteractionResponseType.INFORM_LOSE, message, None)
