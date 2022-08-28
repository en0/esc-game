from abc import ABC, abstractmethod


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

