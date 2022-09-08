from esc.core.exception import ConfigurationError
from esc.core.model import StaticRoomPack
from esc.core.typing import GameObject, RoomCreator, RoomFactory, RoomPack


class RoomPackBuilder:

    class __DelegateRoomFactory(RoomFactory):

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
        factory = RoomPackBuilder.__DelegateRoomFactory(name, creator)
        self._factories.append(factory)
        return self

    def build(self) -> RoomPack:
        if self._name is None:
            raise ConfigurationError("You must specify a name for this RoomPack.")
        return StaticRoomPack(self._name, self._factories)
