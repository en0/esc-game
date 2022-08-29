from typing import List, Callable
from abc import ABC, abstractmethod
from enum import Enum, auto


class ActionReceiver(ABC):

    @abstractmethod
    def begin_interaction(self, name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def end_interaction(self, name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def collect_input(self, message: str, mime_type: str = None) -> str:
        raise NotImplementedError()

    @abstractmethod
    def inform_result(self, message: str, mime_type: str = None) -> None:
        raise NotImplementedError()


class Action(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def trigger(self, owner: "GameObject", receiver: ActionReceiver):
        raise NotImplementedError()


class GameObject(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_summary(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def add_child(self, child: "GameObject") -> None:
        raise NotImplementedError()

    @abstractmethod
    def remove_child(self, name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_child(self, name: str) -> "GameObject":
        raise NotImplementedError()

    @abstractmethod
    def get_children(self) -> List["GameObject"]:
        raise NotImplementedError()

    @abstractmethod
    def add_action(self, action: Action) -> None:
        raise NotImplementedError()

    @abstractmethod
    def list_action_names(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def trigger_action(self, name: str, receiver: ActionReceiver) -> None:
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


class Command(ABC):

    @abstractmethod
    def execute(self):
        raise NotImplementedError()


class RoomPack(ABC):

    @abstractmethod
    def list_room_names(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def create_room(self, name: str) -> GameObject:
        raise NotImplementedError()


class RoomFactory(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def create(self) -> GameObject:
        raise NotImplementedError()


class EscapeRoomGame(ABC):

    @abstractmethod
    def list_room_names(self) -> List[str]:
        raise NotImplementedError()

    # list room names
    # load a game
    # summarize the room
    # inspect object
    # interact object

