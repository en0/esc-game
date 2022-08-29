from esc.core import RoomPackBuilder

from .base import BuilderBase


class RoomPackBuilderBuilder(BuilderBase):

    def build(self) -> RoomPackBuilder:
        return RoomPackBuilder()

