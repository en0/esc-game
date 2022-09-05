from typing import Tuple
from abc import ABC, abstractmethod


class PromptSession(ABC):

    @abstractmethod
    def prompt(self, message: str) -> Tuple[str, str]:
        raise NotImplementedError()

