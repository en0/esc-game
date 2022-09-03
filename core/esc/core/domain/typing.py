from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import (
    Dict,
    List,
    Callable,
    Set,
    Any,
    Generator,
    Iterator,
)


RoomCreator = Callable[[None], "GameObject"]
InteractionResponseGenerator = Generator[
    "InteractionResponse",
    "InteractionResponse",
    "InteractionResponse",
]


class InteractionResponseType(Enum):
    DONE = auto()
    COLLECT_INPUT = auto()
    INFORM_RESULT = auto()
    INFORM_WIN = auto()


class ActionApi(ABC):

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


class InteractionResponse(ABC):

    @abstractmethod
    def get_type(self) -> InteractionResponseType:
        raise NotImplementedError()

    @abstractmethod
    def get_message(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_hits(self) -> Set[str]:
        raise NotImplementedError()


class Interaction(InteractionResponse):

    @abstractmethod
    def __iter__(self) -> Iterator["Interaction"]:
        raise NotImplementedError()

    @abstractmethod
    def __next__(self) -> "Interaction":
        raise NotImplementedError()

    @abstractmethod
    def inform_input(self, value: str) -> None:
        raise NotImplementedError()


class Action(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def trigger(
        self,
        api: ActionApi,
        using_object: "GameObject" = None,
    ) -> InteractionResponseGenerator:
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
    def interact(
        self,
        object_name: str,
        action_name: str,
        using_object: str = None,
    ) -> Interaction:
        raise NotImplementedError()

