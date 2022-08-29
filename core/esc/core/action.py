from .typing import (
    Action,
    GameObject,
    ActionReceiver,
)


class InformAction(Action):

    def __init__(self, name: str, message: str) -> None:
        self._name = name
        self._message = message
        self._owner = None

    def get_name(self) -> str:
        return self._name

    def set_owner(self, owner: GameObject) -> None:
        self._owner = owner

    def trigger(self, receiver: ActionReceiver):
        receiver.inform_response(self._message)

