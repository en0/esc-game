from typing import List, Dict, Any, Set

from .exception import (
    ActionNotFoundError,
    ObjectNotFoundError,
    PropertyNotFoundError,
    RoomPackNotFoundError,
)
from .typing import (
    Action,
    ActionApi,
    GameObject,
    InteractionResponse,
    InteractionResponseGenerator,
    InteractionResponseType,
    RoomFactory,
    RoomPack,
)


class BasicGameObject(GameObject):

    def __init__(
        self,
        name: str,
        aliases: List[str] = None,
        children: List["GameObject"] = None,
        properties: Dict[str, Any] = None,

    ) -> None:
        self._actions = {}
        self._actions_lookup = {}
        self._aliases = aliases or []
        self._children = {}
        self._children_lookup = {}
        self._name = name
        self._props = {k: v for k, v in (properties or {}).items()}
        for child in (children or []):
            self.add_child(child)

    def get_name(self) -> str:
        return self._name

    def get_aliases(self) -> List[str]:
        return list(self._aliases)

    def add_child(self, child: GameObject) -> None:
        name = child.get_name()
        self._children[name] = child
        self._children_lookup[name] = name
        for alias in child.get_aliases():
            self._children_lookup[alias] = name

    def remove_child(self, name: str) -> None:
        try:
            name = self._children_lookup[name]
            del self._children[name]
        except KeyError:
            raise ObjectNotFoundError(name)

    def get_child(self, name: str) -> GameObject:
        try:
            name = self._children_lookup[name]
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
        name = action.get_name()
        self._actions[name] = action
        self._actions_lookup[name] = name
        for alias in action.get_aliases():
            self._actions_lookup[alias] = name

    def get_action(self, name: str) -> Action:
        try:
            name = self._actions_lookup[name]
            return self._actions[name]
        except KeyError:
            raise ActionNotFoundError(self._name, name)

    def list_actions(self) -> List[str]:
        return list(self._actions.keys())


class _InteractionBase(InteractionResponse):
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

    def get_hits(self) -> Set[str]:
        return self._hints


class CompleteInteractionResponse(_InteractionBase):
    def __init__(self) -> None:
        super().__init__(InteractionResponseType.DONE, None, None)


class CollectInputInteractionResponse(_InteractionBase):
    def __init__(self, message: str, hints: Set[str] = None) -> None:
        super().__init__(InteractionResponseType.COLLECT_INPUT, message, hints)


class InformResultInteractionResponse(_InteractionBase):
    def __init__(self, message: str, hints: Set[str] = None) -> None:
        super().__init__(InteractionResponseType.INFORM_RESULT, message, hints)


class InformWinInteractionResponse(_InteractionBase):
    def __init__(self, message: str) -> None:
        super().__init__(InteractionResponseType.INFORM_WIN, message, None)

class InformLoseInteractionResponse(_InteractionBase):
    def __init__(self, message: str) -> None:
        super().__init__(InteractionResponseType.INFORM_LOSE, message, None)


class StaticRoomPack(RoomPack):

    def __init__(self, room_factories: List[RoomFactory]) -> None:
        self._room_factories = {f.get_name(): f for f in room_factories}

    def list_rooms(self) -> List[str]:
        return list(self._room_factories.keys())

    def create_room(self, name: str) -> GameObject:
        try:
            factory = self._room_factories[name]
        except KeyError:
            raise RoomPackNotFoundError(name)
        else:
            return factory.create()
