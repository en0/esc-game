from typing import List, Any, Dict
from esc.core import GameObject, Action
from esc.core.domain.model import BasicGameObject

from .base import BuilderBase


class BasicGameObjectBuilder(BuilderBase[GameObject]):

    def __init__(self) -> None:
        self._name = "name"
        self._children = None
        self._props = dict()
        self._actions = list()
        self._aliases = list()

    def with_name(self, value: str) -> "GameObjectBuilder":
        self._name = value
        return self

    def with_alias(self, value: str) -> "GameObjectBuilder":
        self._aliases.append(value)
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

    def with_action(self, action: Action) -> "GameObjectBuilder":
        self._actions.append(action)
        return self

    def build(self) -> GameObject:
        obj = BasicGameObject(
            name=self._name,
            aliases=self._aliases,
            children=self._children,
            properties=self._props,
        )
        for a in self._actions:
            obj.add_action(a)
        return obj
