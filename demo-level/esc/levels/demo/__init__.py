from typing import List

import pkg_resources
from esc.core.builder import RoomPackBuilder
from esc.core.typing import GameObject, RoomPack

from .loader import YamlGameLoader


class DemoRoomPack(RoomPack):

    def __init__(self):
        self._package = (
            RoomPackBuilder()
            .with_name("Demo")
            .with_room(*self._load_room("Study"))
            .build()
        )

    def get_name(self) -> str:
        return self._package.get_name()

    def list_rooms(self) -> List[str]:
        return self._package.list_rooms()

    def create_room(self, name: str) -> GameObject:
        return self._package.create_room(name)

    def _load_room(self, name: str):
        path = pkg_resources.resource_filename(__package__, f"{name.lower()}.yaml")
        return name, YamlGameLoader(name, path)
