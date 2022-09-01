from typing import Dict, List, Callable, Set, Any, Generator
from contextlib import contextmanager
from abc import ABC, abstractmethod


class Receiver(ABC):

    @abstractmethod
    def inform_win(self, message: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def start_interactive_session(self, sender: str, hints: Set[str]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def end_interactive_session(self, sender: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def collect_input(
        self,
        sender: str,
        prompt: str,
        hints: Set[str] = None
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    def inform_response(
        self,
        sender: str,
        message: str,
    ) -> None:
        raise NotImplementedError()


class InteractiveActionReceiver(ABC):

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


class ActionReceiver(ABC):

    @abstractmethod
    def win(self, message: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_owner_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def set_object_property(self, object_name: str, key: str, value: Any) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_object_property(self, object_name: str, key: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def reveal_child_object(self, object_name: str, child_name: str) -> None:
        raise NotImplementedError()

    @contextmanager
    @abstractmethod
    def interactive_session(
        self,
        hints: Set[str] = None
    ) -> Generator[InteractiveActionReceiver, None, None]:
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
    def trigger(self, receiver: ActionReceiver):
        raise NotImplementedError()


class GameObject(ABC):

    @abstractmethod
    def get_name(self) -> str:
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
    def get_property(self, key: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def set_property(self, key: str, value: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def add_action(self, action: Action) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_action(self, name: str) -> Action:
        raise NotImplementedError()

    @abstractmethod
    def list_actions(self) -> List[str]:
        raise NotImplementedError()


RoomCreator = Callable[None, GameObject]


class Command(ABC):

    @abstractmethod
    def execute(self):
        raise NotImplementedError()


class RoomPack(ABC):

    @abstractmethod
    def list_rooms(self) -> List[str]:
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
    def load_room(self, name: str) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def get_object_actions(self) -> Dict[str, List[str]]:
        raise NotImplementedError()

    @abstractmethod
    def make_action_command(
        self,
        object_name: str,
        action_name: str,
        using_object: str = None,
    ) -> Command:
        raise NotImplementedError()

