from esc.core import GameObjectBuilder
from .base import BuilderBase


class GameObjectBuilderBuidler(BuilderBase):

    def build(self) -> GameObjectBuilder:
        return GameObjectBuilder()
