from dataclasses import dataclass
from typing import Any, Dict, List

from esc.core.builder import GameObjectBuilder
from esc.core.typing import GameObject

from . import action as all_actions


@dataclass
class InformActionSpec:
    message: str
    aliases: List[str] = None
    key: str = None
    reveals_children: bool = False

    @staticmethod
    def from_dict(data: Dict) -> "InformActionSpec":
        return InformActionSpec(
            message=data["message"],
            aliases=list(data.get("aliases", ["inspect", "examine"])),
            key=data.get("key"),
            reveals_children=data.get("reveals_children", False)
        )


@dataclass
class PropertySpec:
    key: str
    value: Any

    @staticmethod
    def from_dict(data: Dict) -> "PropertySpec":
        return PropertySpec(
            key=data["key"],
            value=data["value"],
        )


@dataclass
class GameObjectSpec:

    name: str
    aliases: List[str] = None
    inform_actions: List[InformActionSpec] = None
    actions: List[str] = None
    properties: List[PropertySpec] = None
    children: List["GameObjectSpec"] = None

    def build(self, constant: Dict = None) -> GameObject:
        constant = constant or {}
        builder = GameObjectBuilder()
        builder.with_name(self.name)
        for alias in self.aliases or []:
            builder.with_alias(alias)
        for inform_action in self.inform_actions or []:
            builder.with_inform_action(
                inform_action.message,
                inform_action.aliases,
                inform_action.key)
            if inform_action.reveals_children:
                builder.and_with_reveal_decorator()
        for action in self.actions:
            klass = getattr(all_actions, action)
            builder.with_action(klass(constant))
        for prop in self.properties or []:
            builder.with_property(prop.key, prop.value)
        for child in self.children or []:
            builder.with_child(child.build())
        return builder.build()

    @staticmethod
    def from_dict(data: Dict) -> "GameObjectSpec":
        return GameObjectSpec(
            name=data["name"],
            aliases=data.get("aliases"),
            inform_actions=[
                InformActionSpec.from_dict(a)
                for a in data.get("inform_actions", [])
            ],
            actions=list(data.get("actions", [])),
            properties=[
                PropertySpec.from_dict(a)
                for a in data.get("properties", [])
            ],
            children=[
                GameObjectSpec.from_dict(a)
                for a in data.get("children", [])
            ],
        )
