from esc.core import Game
from esc.core.usecase import GameInteractor

from .base import BuilderBase


class GameInteractorBuilder(BuilderBase[Game]):

    def build(self) -> Game:
        return GameInteractor()

