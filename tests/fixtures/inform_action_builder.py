from esc.core import InformAction

from .base import BuilderBase


class InformActionBuilder(BuilderBase):

    def __init__(self) -> None:
        self._message = None
        self._property = None
        self._name = "action-name"
        self._aliases = []

    def with_default_message(self, value: str) -> "InformActionBuilder":
        self._message = value
        return self

    def with_property_key(self, value: str) -> "InformActionBuilder":
        self._property = value
        return self

    def with_name(self, value: str) -> "InformActionBuilder":
        self._name = value
        return self

    def with_alias(self, value: str) -> "InformActionBuilder":
        self._aliases.append(value)
        return self

    def build(self) -> InformAction:
        return InformAction(
            name=self._name,
            aliases=self._aliases,
            property=self._property,
            default_message=self._message,
        )
