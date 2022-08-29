from typing import Dict, List, Callable, Set
from abc import ABC, abstractmethod


class Receiver(ABC):

    @abstractmethod
    def receive_object_action_list(self, object_names: Dict[str, List[str]]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def inform_win(self, message: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def initialize_receiver(self, sender_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def shutdown_receiver(self, sender_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def collect_input(
        self,
        sender_name: str,
        prompt: str,
        hints: Set[str] = None
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    def inform_response(
        self,
        sender_name: str,
        message: str,
    ) -> None:
        raise NotImplementedError()


class ActionReceiver(ABC):

    @abstractmethod
    def win(self, message: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def collect_input(
        self,
        prompt: str,
        hints: Set[str] = None
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    def inform_response(
        self,
        message: str,
    ) -> None:
        raise NotImplementedError()


class Action(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def set_owner(self) -> str:
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


RoomCreator = Callable[None, GameObject]


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
    ...

    # list room names
    # load a game
    # summarize the room
    # inspect object
    # interact object


