from typing import Any, List

from .domain import (Action, BasicGameObject, ConfigurationError, EscapeRoomGame, GameObject,
                     InformAction, RevealActionDecorator, RoomCreator, RoomFactory, RoomPack,
                     StaticRoomPack)
from .interactor import EscapeRoomGameInteractor


class GameObjectBuilder:

    def __init__(self) -> None:
        self._last_added_action = None
        self._actions = []
        self._aliases = []
        self._children = []
        self._name = None
        self._props = {}

    def with_name(self, value: str) -> "GameObjectBuilder":
        self._name = value
        return self

    def with_alias(self, value: str) -> "GameObjectBuilder":
        self._aliases.append(value)
        return self

    def with_children(self, value: List[GameObject]) -> "GameObjectBuilder":
        for child in value:
            self.with_child(child)
        return self

    def with_child(self, value: GameObject) -> "GameObjectBuilder":
        self._children.append(value)
        return self

    def with_property(self, key: str, value: Any) -> "GameObjectBuilder":
        self._props[key] = value
        return self

    def with_action(self, value: Action) -> "GameObjectBuilder":
        self._actions.append(value)
        self._last_added_action = value
        return self

    def with_inform_action(
        self,
        value: str,
        aliases: List[str],
        prop_key: str = "_inspect_msg",
    ) -> "GameObjectBuilder":
        name, *aliases = aliases
        self.with_action(InformAction(name, aliases, prop_key, value))
        return self

    def and_with_reveal_decorator(self) -> "GameObjectBuilder":
        if self._last_added_action is None:
            raise ConfigurationError(
                "You can only add a decorator after adding an action to decorate.")
        self.with_action(RevealActionDecorator(self._last_added_action))
        return self

    def build(self) -> GameObject:
        if self._name is None:
            raise ConfigurationError("Name is required to build a game object.")
        go = BasicGameObject(
            name=self._name,
            aliases=self._aliases,
            children=list(self._children),
            properties=self._props
        )
        for action in self._actions:
            go.add_action(action)
        return go


class RoomPackBuilder:

    class _DelegateRoomFactory(RoomFactory):

        def __init__(self, name: str, create: RoomCreator) -> None:
            self._name = name
            self._create = create

        def get_name(self) -> str:
            return self._name

        def create(self) -> GameObject:
            return self._create()

    def __init__(self) -> None:
        self._name = None
        self._factories = []

    def with_name(self, name: str) -> "RoomPackBuilder":
        self._name = name
        return self

    def with_room(self, name: str, creator: RoomCreator) -> "RoomPackBuilder":
        factory = RoomPackBuilder._DelegateRoomFactory(name, creator)
        self._factories.append(factory)
        return self

    def build(self) -> RoomPack:
        if self._name is None:
            raise ConfigurationError("You must specify a name for this RoomPack.")
        return StaticRoomPack(self._name, self._factories)


class EscapeRoomGameBuilder:

    def __init__(self) -> None:
        self._room_pack = None

    def with_room_pack(self, value: RoomPack) -> "EscapeRoomGameBuilder":
        self._room_pack = value
        return self

    def build(self) -> EscapeRoomGame:
        if self._room_pack:
            return EscapeRoomGameInteractor(self._room_pack)
        raise ConfigurationError("You must specify a RoomPack")
