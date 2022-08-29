from esc.core import EscapeRoomGame
from esc.core.usecase import EscapeRoomGameInteractor

from .base import BuilderBase


class EscapeRoomGameInteractorBuilder(BuilderBase[EscapeRoomGame]):

    def build(self) -> EscapeRoomGame:
        return EscapeRoomGameInteractor()

