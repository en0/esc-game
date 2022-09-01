from typing import List, Callable, Any
from .exception import ConfigurationError
from .model import StaticRoomPack, BasicGameObject
from .interactor import EscapeRoomGameInteractor
from .typing import (
    Action,
    EscapeRoomGame,
    GameObject,
    Receiver,
    RoomCreator,
    RoomFactory,
    RoomPack,
)


class GameObjectBuilder:

    def __init__(self) -> None:
        self._actions = []
        self._children = []
        self._name = None
        self._props = {}

    def with_name(self, value: str) -> "GameObjectBuilder":
        self._name = value
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
        return self

    def build(self) -> GameObject:
        if self._name is None:
            raise ConfigurationError("Name is required to build a game object.")
        go = BasicGameObject(self._name, list(self._children), self._props)
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
        self._factories = []

    def with_room_container(self, name: str, creator: RoomCreator) -> "RoomPackBuilder":
        factory = RoomPackBuilder._DelegateRoomFactory(name, creator)
        self._factories.append(factory)

    def build(self) -> RoomPack:
        return StaticRoomPack(self._factories)


class EscapeRoomGameBuilder:

    def __init__(self) -> None:
        self._room_pack = None
        self._receiver = None

    def with_room_pack(self, value: RoomPack) -> "EscapeRoomGameBuilder":
        self._room_pack = value

    def with_receiver(self, value: Receiver) -> "EscapeRoomGameBuilder":
        self._receiver = value

    def build(self) -> EscapeRoomGame:
        if self._receiver and self._room_pack:
            return EscapeRoomGameInteractor(self._room_pack, self._receiver)
        raise ConfigurationError("You must specifiy a Receiver and a RoomPack")
