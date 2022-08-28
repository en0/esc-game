from typing import List
from esc.core.domain import Room

from .base import BuilderBase


class RoomBuilder(BuilderBase[Room]):

    def build(self) -> Room:
        return Room(self._name)

    def with_name(self, value: str) -> "GameObjectBuilder":
        self._name = value
        return self

    def __init__(self) -> None:
        self._name = "name"

