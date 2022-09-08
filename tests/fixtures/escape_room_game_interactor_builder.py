from esc.core.interactor import EscapeRoomGameInteractor
from esc.core.typing import EscapeRoomGame, RoomPack

from .base import BuilderBase


class EscapeRoomGameInteractorBuilder(BuilderBase[EscapeRoomGame]):

    def __init__(self) -> None:
        self._room_pack = None

    def with_room_pack(self, room_pack: RoomPack) -> "EscapeRoomGameInteractorBuilder":
        self._room_pack = room_pack
        return self

    def build(self) -> EscapeRoomGame:
        if self._room_pack:
            return EscapeRoomGameInteractor(self._room_pack)
        raise ValueError("You must specify a RoomPack")

