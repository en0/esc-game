from esc.core import InformAction, GameObject

from .base import BuilderBase


class InformActionBuilder(BuilderBase):

    def __init__(self) -> None:
        self._message = ""
        self._name = "action-name"

    def with_name(self, value: str) -> "InformActionBuilder":
        self._name = value
        return self

    def with_message(self, value: str) -> "InformActionBuilder":
        self._message = value
        return self

    def build(self) -> InformAction:
        return InformAction(self._name, self._message)

