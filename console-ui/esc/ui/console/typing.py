from abc import ABC, abstractmethod
from typing import List, Tuple


class GamePrompt(ABC):

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def prompt_for_action(self, room: str) -> Tuple[str, str]:
        raise NotImplementedError()

    @abstractmethod
    def prompt_for_interaction(self, message: str, object_name: str = None, hidden: bool = False) -> str:
        raise NotImplementedError()

    @abstractmethod
    def prompt_with_choices(self, message: str, choices: List[str]):
        raise NotImplementedError()
