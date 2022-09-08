from typing import Any, Dict, List

from esc.core.exception import (ActionNotFoundError, ObjectNotFoundError, PropertyNotFoundError)
from esc.core.typing import (Action, GameObject)


class BasicGameObject(GameObject):

    def __init__(
            self,
            name: str,
            aliases: List[str] = None,
            children: List["GameObject"] = None,
            properties: Dict[str, Any] = None,

    ) -> None:
        self._actions = {}
        self._actions_lookup = {}
        self._aliases = aliases or []
        self._children = {}
        self._children_lookup = {}
        self._name = name
        self._props = {k: v for k, v in (properties or {}).items()}
        for child in (children or []):
            self.add_child(child)

    def get_name(self) -> str:
        return self._name

    def get_aliases(self) -> List[str]:
        return list(self._aliases)

    def add_child(self, child: GameObject) -> None:
        name = child.get_name()
        self._children[name] = child
        self._children_lookup[name] = name
        for alias in child.get_aliases():
            self._children_lookup[alias] = name

    def remove_child(self, name: str) -> None:
        try:
            name = self._children_lookup[name]
            del self._children[name]
        except KeyError:
            raise ObjectNotFoundError(name)

    def get_child(self, name: str) -> GameObject:
        try:
            name = self._children_lookup[name]
            return self._children[name]
        except KeyError:
            raise ObjectNotFoundError(name)

    def get_children(self) -> List["GameObject"]:
        return list(self._children.values())

    def get_property(self, key: str) -> Any:
        try:
            return self._props[key]
        except KeyError:
            raise PropertyNotFoundError(self._name, key)

    def set_property(self, key: str, value: Any) -> Any:
        self._props[key] = value

    def add_action(self, action: Action) -> None:
        name = action.get_name()
        self._actions[name] = action
        self._actions_lookup[name] = name
        for alias in action.get_aliases():
            self._actions_lookup[alias] = name

    def get_action(self, name: str) -> Action:
        try:
            name = self._actions_lookup[name]
            return self._actions[name]
        except KeyError:
            raise ActionNotFoundError(self._name, name)

    def list_actions(self) -> List[str]:
        return list(self._actions.keys())
