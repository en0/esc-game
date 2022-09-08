from esc.core import ActionApi, GameObject
from esc.core.interactor import ActionReceiverInteractor

from .base import BuilderBase
from .basic_game_object_builder import BasicGameObjectBuilder


class ActionReceiverInteractorBuilder(BuilderBase):

    def __init__(self) -> None:
        self._room = BasicGameObjectBuilder().build()
        self._sender = BasicGameObjectBuilder().with_name("unittest").build()

    def with_room(self, room: GameObject) -> "BasicActionReceiverBuilder":
        self._room = room
        return self

    def with_sender(self, sender: GameObject) -> "BasicActionReceiverBuilder":
        self._sender = sender
        return self

    def build(self) -> ActionApi:
        return ActionReceiverInteractor(self._room, self._sender)
