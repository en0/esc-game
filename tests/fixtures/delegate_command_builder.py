from typing import List, Dict, Callable
from esc.core import Command
from esc.core.model import DelegateCommand

from .base import BuilderBase


class DelegateCommandBuilder(BuilderBase[Command]):

    def build(self) -> Command:
        return DelegateCommand(self._delegate, *self._args, **self._kwargs)

    def with_delegate(self, value: Callable) -> "GameObjectBuilder":
        self._delegate = value
        return self

    def with_args(self, *value: List[str]) -> "GameObjectBuilder":
        self._args = value
        return self

    def with_kwargs(self, **value: Dict[str, any]) -> "GameObjectBuilder":
        self._kwargs = value
        return self

    def __init__(self) -> None:
        self._args = []
        self._kwargs = {}
        self._delegate = self._noop_delegate

    def _noop_delegate(self, *args, **kwargs) -> None:
        ...

