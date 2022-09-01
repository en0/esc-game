from esc.core import EscapeRoomGame, RoomPack, Receiver
from esc.core.interactor import EscapeRoomGameInteractor

from .base import BuilderBase


class EscapeRoomGameInteractorBuilder(BuilderBase[EscapeRoomGame]):

    def __init__(self) -> None:
        self._room_pack = None
        self._receiver = None

    def with_receiver(self, receiver: Receiver) -> "EscapeRoomGameInteractorBuilder":
        self._receiver = receiver
        return self

    def with_room_pack(self, room_pack: RoomPack) -> "EscapeRoomGameInteractorBuilder":
        self._room_pack = room_pack
        return self

    def build(self) -> EscapeRoomGame:
        if self._room_pack is None or self._receiver is None:
            raise ValueError("You must specify a RoomPack and Receiver")
        return EscapeRoomGameInteractor(self._room_pack, self._receiver)

