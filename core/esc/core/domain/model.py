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
        children: List["GameObject"] = None,
        properties: Dict[str, Any] = None,

    ) -> None:
        self._name = name
        self._children = {c.get_name(): c for c in children or []}
        self._props = {k: v for k, v in (properties or {}).items()}
        self._actions = {}

    def get_name(self) -> str:
        return self._name

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

    def get_action(self, name: str) -> Action:
        try:
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
