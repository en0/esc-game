from typing import List
from .abstractions import Interaction, InteractionReceiver
from .exceptions import ObjectNotInteractable


class GameObject:

    def __init__(
        self,
        name: str,
        details: str,
        summary: str,
        children: List["GameObject"] = None
    ) -> None:
        self._name = name
        self._details = details
        self._summary = summary
        self._children = children or []
        self._interaction = None

    def get_name(self) -> str:
        return self._name

    def get_details(self) -> str:
        return self._details

    def get_summary(self) -> str:
        return self._summary

    def get_children(self) -> List["GameObject"]:
        return self._children

    def set_interaction(self, interaction: Interaction) -> None:
        self._interaction = interaction

    def interact(self, receiver: InteractionReceiver) -> None:
        if self._interaction is None:
            raise ObjectNotInteractable(self._name)
        self._interaction.interact(receiver)

