from typing import List, Dict, Set, Generator, Any
from contextlib import contextmanager
from .model import DelegateCommand
from .typing import (
    Action,
    ActionReceiver,
    Command,
    EscapeRoomGame,
    GameObject,
    InteractiveActionReceiver,
    Receiver,
    RoomPack,
)


class EscapeRoomGameInteractor(EscapeRoomGame):

    def __init__(self, room_pack: RoomPack, receiver: Receiver) -> None:
        self._room_pack = room_pack
        self._receiver = receiver
        self._room = None

    def load_room(self, name: str) -> List[str]:
        self._room = self._room_pack.create_room(name)

    def get_object_actions(self) -> Dict[str, List[str]]:
        raise NotImplementedError()

    def make_action_command(
        self,
        object_name: str,
        action_name: str,
        using_object: str = None,
    ) -> Command:
        obj = self._room.get_child(object_name)
        act = obj.get_action(action_name)
        return DelegateCommand(self._trigger_action, obj, act)

    def _trigger_action(game_object: GameObject, action: Action):
        raise NotImplementedError()


class ActionReceiverInteractor(ActionReceiver, InteractiveActionReceiver):

    def __init__(self, receiver: Receiver, room: GameObject, sender: GameObject) -> None:
        self._receiver = receiver
        self._container = room
        self._sender_name = sender.get_name()

    def win(self, message: str) -> None:
        self._receiver.inform_win(message)

    def set_object_property(self, object_name: str, key: str, value: Any) -> None:
        obj = self._container.get_child(object_name)
        obj.set_property(key, value)

    def get_object_property(self, object_name: str, key: str) -> None:
        obj = self._container.get_child(object_name)
        return obj.get_property(key)

    def reveal_child_object(self, object_name: str, child_name: str) -> None:
        obj = self._container.get_child(object_name)
        new_obj = obj.get_child(child_name)
        self._container.add_child(new_obj)

    @contextmanager
    def interactive_session(
        self,
        hints: Set[str] = None
    ) -> Generator[InteractiveActionReceiver, None, None]:
        self._receiver.start_interactive_session(self._sender_name, hints)
        try:
            yield self
        finally:
            self._receiver.end_interactive_session(self._sender_name)

    def collect_input(
        self,
        prompt: str,
        hints: Set[str] = None
    ) -> str:
        return self._receiver.collect_input(self._sender_name, prompt, hints)

    def inform_response(
        self,
        message: str,
    ) -> None:
        self._receiver.inform_response(self._sender_name, message)

