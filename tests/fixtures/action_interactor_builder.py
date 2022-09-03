from esc.core import Interaction, InteractionResponseGenerator
from esc.core.interactor import ActionInteractor

from .base import BuilderBase


class ActionInteractorBuilder(BuilderBase):

    def __init__(self):
        self._generator = iter([])
        self._object = "some-object"
        self._action = "some-action"

    def with_generator(self, value: InteractionResponseGenerator) -> "ActionInteractorBuilder":
        self._generator = value
        return self

    def with_object_name(self, value: str) -> "ActionInteractorBuilder":
        self._object = value
        return self

    def with_action_name(self, value: str) -> "ActionInteractorBuilder":
        self._action = value
        return self

    def build(self) -> Interaction:
        return ActionInteractor(self._generator, self._object, self._action)
