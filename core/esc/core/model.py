from typing import List, Dict, Callable, Any

from .exception import (
    ActionError,
    ActionNotFoundError,
    NotInteractableError,
    ObjectNotFoundError,
    PropertyNotFoundError,
    RoomPackNotFoundError,
)
from .typing import (
    Action,
    Command,
    GameObject,
    ActionReceiver,
    RoomFactory,
    RoomPack,
)


class BasicGameObject(GameObject):

    def __init__(
        self,
        name: str,
        summary: str,
        children: List["GameObject"] = None,
        properties: Dict[str, Any] = None,

    ) -> None:
        self._name = name
        self._summary = summary
        self._children = {c.get_name(): c for c in children or []}
        self._props = {k: v for k, v in properties.items()}
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
            raise ObjectNotFoundError(name)

    def get_child(self, name: str) -> GameObject:
        try:
            return self._children[name]
        except KeyError:
            raise ObjectNotFoundError(name)

    def get_children(self) -> List["GameObject"]:
        return list(self._children.values())

    def get_property(self, key: str) -> Any:
        try:
            return self._props[key]
        except KeyError:
            raise PropertyNotFoundError(self._name, key)

    def set_property(self, key: str, value: Any) -> Any:
        self._props[key] = value

    def add_action(self, action: Action) -> None:
        self._actions[action.get_name()] = action
        action.set_owner(self)

    def list_action_names(self) -> List[str]:
        return list(self._actions.keys())

    def trigger_action(self, name: str, receiver: ActionReceiver) -> None:
        if name not in self._actions:
            raise ActionNotFoundError(self._name, name)
        try:
            self._actions[name].trigger(receiver)
        except Exception:
            raise ActionError(self._name, name)


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

    def create_room(self, name: str) -> GameObject:
        try:
            factory = self._room_factories[name]
        except KeyError:
            raise RoomPackNotFoundError(name)
        else:
            return factory.create()

