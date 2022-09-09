from esc.core.interactor.action_api_interactor import ActionApiInteractor
from esc.core.typing import ActionApi, GameObject

from .base import BuilderBase
from .basic_game_object_builder import BasicGameObjectBuilder


class ActionApiInteractorBuilder(BuilderBase):

    def __init__(self) -> None:
        self._room = BasicGameObjectBuilder().build()
        self._sender = BasicGameObjectBuilder().with_name("unittest").build()

    def with_room(self, room: GameObject) -> "ActionApiInteractorBuilder":
        self._room = room
        return self

    def with_sender(self, sender: GameObject) -> "ActionApiInteractorBuilder":
        self._sender = sender
        return self

    def build(self) -> ActionApi:
        return ActionApiInteractor(self._room, self._sender)
