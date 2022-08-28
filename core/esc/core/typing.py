from typing import List
from abc import ABC, abstractmethod
from enum import Enum, auto


class TargetTypeEnum(Enum):
    GAME_OBJECT = auto()
    ROOM = auto()


class ActionEnum(Enum):
    INSPECT = auto()
    INTERACT = auto()



class InteractionReceiver(ABC):

    @abstractmethod
    def begin_interaction(self, name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def end_interaction(self, name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def collect_input(self, message: str, tag: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def inform_result(self, message: str, tag: str) -> None:
        raise NotImplementedError()


class Interaction(ABC):

    @abstractmethod
    def interact(self, receiver: InteractionReceiver):
        raise NotImplementedError()


class GameObject(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_details(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_summary(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_children(self) -> List["GameObject"]:
        raise NotImplementedError()

    @abstractmethod
    def set_interaction(self, interaction: Interaction) -> None:
        raise NotImplementedError()

    @abstractmethod
    def interact(self, receiver: InteractionReceiver) -> None:
        raise NotImplementedError()


class Room(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_summary(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def add_game_object(self, game_object: GameObject) -> None:
        raise NotImplementedError()

    @abstractmethod
    def list_object_names(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_game_object(self, game_object_name: str) -> GameObject:
        raise NotImplementedError()


class GameReceiver(ABC):

    @abstractmethod
    def enter_room(self, room_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def exit_room(self, room_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def summarize_room(self, room_summary: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def summarize_inspection(self, inspection_summary: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def notify_unknown_target(
        self,
        target_name: str,
        target_type: TargetTypeEnum
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def notify_unknown_action(
        self,
        target_name: str,
        target_type: TargetTypeEnum,
        action: ActionEnum
    ) -> None:
        raise NotImplementedError()


class Command(ABC):

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

class Game(ABC):
    ...

