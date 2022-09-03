from esc.core import Interaction, InteractionResponseGenerator
from esc.core.interactor import ActionInteractor

from .base import BuilderBase


class ActionInteractorBuilder(BuilderBase):

    def __init__(self):
        self._generator = iter([])

    def with_generator(self, value: InteractionResponseGenerator) -> "ActionInteractorBuilder":
        self._generator = value
        return self

    def build(self) -> Interaction:
        return ActionInteractor(self._generator)
