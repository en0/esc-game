from typing import Any, List

from esc.core.action import InformAction, RevealActionDecorator
from esc.core.exception import ConfigurationError
from esc.core.model import BasicGameObject
from esc.core.typing import Action, GameObject


class GameObjectBuilder:

    def __init__(self) -> None:
        self._last_added_action = None
        self._actions = []
        self._aliases = []
        self._children = []
        self._name = None
        self._props = {}

    def with_name(self, value: str) -> "GameObjectBuilder":
        self._name = value
        return self

    def with_alias(self, value: str) -> "GameObjectBuilder":
        self._aliases.append(value)
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
        self._last_added_action = value
        return self

    def with_inform_action(
            self,
            value: str,
            aliases: List[str],
            prop_key: str = "_inspect_msg",
    ) -> "GameObjectBuilder":
        name, *aliases = aliases
        self.with_action(InformAction(name, aliases, prop_key, value))
        return self

    def and_with_reveal_decorator(self) -> "GameObjectBuilder":
        if self._last_added_action is None:
            raise ConfigurationError(
                "You can only add a decorator after adding an action to decorate.")
        self.with_action(RevealActionDecorator(self._last_added_action))
        return self

    def build(self) -> GameObject:
        if self._name is None:
            raise ConfigurationError("Name is required to build a game object.")
        game_object = BasicGameObject(
            name=self._name,
            aliases=self._aliases,
            children=list(self._children),
            properties=self._props
        )
        for action in self._actions:
            game_object.add_action(action)
        return game_object
