from typing import List
from .abstractions import Interaction, InteractionReceiver, GameObject, Room
from .exceptions import NotInteractableError, NotFoundError


class BasicGameObject(GameObject):

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
            raise NotInteractableError(self._name)
        self._interaction.interact(receiver)


class BasicRoom(Room):

    def __init__(self, name: str) -> None:
        self._name = name
        self._game_objects = dict()

    def get_name(self) -> str:
        return self._name

    def get_summary(self) -> str:
        return " ".join([o.get_summary() for o in self._game_objects.values()])

    def add_game_object(self, game_object: GameObject) -> None:
        self._game_objects[game_object.get_name()] = game_object

    def list_object_names(self) -> List[str]:
        return list(self._game_objects.keys())

    def get_game_object(self, game_object_name: str) -> GameObject:
        try:
            return self._game_objects[game_object_name]
        except KeyError:
            raise NotFoundError(self._name)


