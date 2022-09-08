from abc import ABC, abstractmethod
from typing import Tuple


class PromptSession(ABC):

    @abstractmethod
    def prompt(self, message: str) -> Tuple[str, str]:
        raise NotImplementedError()

