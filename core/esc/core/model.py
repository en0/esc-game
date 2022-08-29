from typing import List, Dict, Callable

from .exception import NotInteractableError, NotFoundError, ActionError
from .typing import (
    Action,
    Command,
    GameObject,
    ActionReceiver,
    Room,
    RoomFactory,
    RoomPack,
)


class InformAction(Action):

    def __init__(self, name: str, message: str, mime_type: str) -> None:
        self._name = name
        self._message = message
        self._mime_type = mime_type

    def get_name(self) -> str:
        return self._name

    def trigger(self, owner: GameObject, receiver: ActionReceiver):
        receiver.inform_result(self._message, self._mime_type)


class BasicGameObject(GameObject):

    def __init__(
        self,
        name: str,
        summary: str,
        children: List["GameObject"] = None
    ) -> None:
        self._name = name
        self._summary = summary
        self._children = {c.get_name(): c for c in children or []}
        self._actions = {}

    def get_name(self) -> str:
        return self._name

    def get_summary(self) -> str:
        return self._summary

    def add_child(self, child: GameObject) -> None:
        self._children[child.get_name()] = child

    def remove_child(self, name: str) -> None:
        try:
            del self._children[name]
        except KeyError:
            raise NotFoundError(name)

    def get_child(self, name: str) -> GameObject:
        try:
            return self._children[name]
        except KeyError:
            raise NotFoundError(name)

    def get_children(self) -> List["GameObject"]:
        return list(self._children.values())

    def add_action(self, action: Action) -> None:
        self._actions[action.get_name()] = action

    def list_action_names(self) -> List[str]:
        return list(self._actions.keys())

    def trigger_action(self, name: str, receiver: ActionReceiver) -> None:
        if name not in self._actions:
            raise NotFoundError(name)
        try:
            self._actions[name].trigger(self, receiver)
        except Exception:
            raise ActionError(self._name, name)


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


class DelegateCommand(Command):

    def __init__(
        self,
        delegate: Callable,
        *args: List,
        **kwargs: Dict
    ) -> None:
        self._delegate = delegate
        self._args = args
        self._kwargs = kwargs

    def execute(self):
        self._delegate(*self._args, **self._kwargs)


class StaticRoomPack(RoomPack):

    def __init__(self, room_factories: List[RoomFactory]) -> None:
        self._room_factories = {f.get_name(): f for f in room_factories}

    def list_room_names(self) -> List[str]:
        return list(self._room_factories.keys())

    def create_room(self, name: str) -> Room:
        try:
            factory = self._room_factories[name]
        except KeyError:
            raise NotFoundError(name)
        else:
            return factory.create()

