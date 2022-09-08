from esc.core.builder import GameObjectBuilder

from .base import BuilderBase


class GameObjectBuilderBuidler(BuilderBase):

    def build(self) -> GameObjectBuilder:
        return GameObjectBuilder()
