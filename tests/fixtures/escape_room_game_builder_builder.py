from esc.core.builder import EscapeRoomGameBuilder

from .base import BuilderBase


class EscapeRoomGameBuilderBuilder(BuilderBase):

    def build(self) -> EscapeRoomGameBuilder:
        return EscapeRoomGameBuilder()
