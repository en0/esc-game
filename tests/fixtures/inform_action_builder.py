from esc.core import InformAction

from .base import BuilderBase


class InformActionBuilder(BuilderBase):

    def __init__(self) -> None:
        self._message = ""
        self._name = "action-name"
        self._mime_type = None

    def with_name(self, value: str) -> "InformActionBuilder":
        self._name = value
        return self

    def with_message(self, value: str) -> "InformActionBuilder":
        self._message = value
        return self

    def with_mime_type(self, value: str) -> "InformActionBuilder":
        self._mime_type = value
        return self

    def build(self) -> InformAction:
        return InformAction(self._name, self._message, self._mime_type)

