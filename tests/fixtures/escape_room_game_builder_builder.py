from esc.core import EscapeRoomGameBuilder

from .base import BuilderBase


class EscapeRoomGameBuilderBuilder(BuilderBase):

    def build(self) -> EscapeRoomGameBuilder:
        return EscapeRoomGameBuilder()
