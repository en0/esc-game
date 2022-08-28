from typing import List
from esc.core import Room
from esc.core.models import BasicRoom

from .base import BuilderBase


class BasicRoomBuilder(BuilderBase[Room]):

    def build(self) -> Room:
        return BasicRoom(self._name)

    def with_name(self, value: str) -> "GameObjectBuilder":
        self._name = value
        return self

    def __init__(self) -> None:
        self._name = "name"

