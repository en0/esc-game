from typing import List, Any, Dict
from esc.core import GameObject
from esc.core.model import BasicGameObject

from .base import BuilderBase


class BasicGameObjectBuilder(BuilderBase[GameObject]):

    def build(self) -> GameObject:
        return BasicGameObject(
            name=self._name,
            summary=self._summary,
            children=self._children,
            properties=self._props,
        )

    def with_name(self, value: str) -> "GameObjectBuilder":
        self._name = value
        return self

    def with_summary(self, value: str) -> "GameObjectBuilder":
        self._summary = value
        return self

    def with_children(self, value: List[GameObject]) -> "GameObjectBuilder":
        self._children = value
        return self

    def with_property(self, key: str, value: Any) -> "GameObjectBuilder":
        self._props[key] = value
        return self

    def with_properties(self, values: Dict[str, Any]) -> "GameObjectBuilder":
        self._props = {k: v for k, v in values.items()}
        return self

    def __init__(self) -> None:
        self._name = "name"
        self._summary = "summary"
        self._children = None
        self._props = dict()

