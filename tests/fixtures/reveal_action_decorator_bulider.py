from unittest.mock import Mock

from esc.core.action import RevealActionDecorator
from esc.core.typing import Action

from .base import BuilderBase


class RevealActionDecoratorBuilder(BuilderBase[RevealActionDecorator]):

    def __init__(self) -> None:
        self._action = Mock(spec=Action)

    def with_action(self, value: Action) -> "RevealActionDecoratorBuilder":
        self._action = value
        return self

    def build(self) -> RevealActionDecorator:
        return RevealActionDecorator(self._action)
