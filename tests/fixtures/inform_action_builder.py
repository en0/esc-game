from esc.core import GameObject, InformAction

from .base import BuilderBase


class InformActionBuilder(BuilderBase):

    def __init__(self) -> None:
        self._message = None
        self._property = None
        self._name = "action-name"

    def with_default_message(self, value: str) -> "InformActionBuilder":
        self._message = value
        return self

    def with_property_key(self, value: str) -> "InformActionBuilder":
        self._property = value
        return self

    def with_name(self, value: str) -> "InformActionBuilder":
        self._name = value
        return self

    def build(self) -> InformAction:
        return InformAction(self._name, self._property, self._message)
