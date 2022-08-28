from abc import ABC, abstractmethod
from typing import Generic, TypeVar


Build_T = TypeVar("Build_T")


class BuilderBase(Generic[Build_T]):

    @abstractmethod
    def build(self) -> Build_T:
        raise NotImplementedError()
