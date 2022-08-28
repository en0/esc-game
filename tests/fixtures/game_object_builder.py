from typing import List
from esc.core.domain import GameObject

from .base import BuilderBase


class GameObjectBuilder(BuilderBase[GameObject]):

    def build(self) -> GameObject:
        return GameObject(
            name=self._name,
            details=self._details,
            summary=self._summary,
            children=self._children,
        )

    def with_name(self, value: str) -> "GameObjectBuilder":
        self._name = value
        return self

    def with_details(self, value: str) -> "GameObjectBuilder":
        self._details = value
        return self

    def with_summary(self, value: str) -> "GameObjectBuilder":
        self._summary = value
        return self

    def with_children(self, value: List[GameObject]) -> "GameObjectBuilder":
        self._children = value
        return self

    def __init__(self) -> None:
        self._name = "name"
        self._details = "details"
        self._summary = "summary"
        self._children = None

