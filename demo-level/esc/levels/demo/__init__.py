from typing import List
from esc.core import RoomPackBuilder, RoomPack, GameObject

from . import study


class DemoRoomPack(RoomPack):

    def __init__(self):
        self._package = (
            RoomPackBuilder()
            .with_name("Demo")
            .with_room(study.name, study.creator)
            .build()
        )

    def get_name(self) -> str:
        return self._package.get_name()

    def list_rooms(self) -> List[str]:
        return self._package.list_rooms()

    def create_room(self, name: str) -> GameObject:
        return self._package.create_room(name)

