from esc.core.exception import ConfigurationError
from esc.core.interactor import EscapeRoomGameInteractor
from esc.core.typing import EscapeRoomGame, RoomPack


class EscapeRoomGameBuilder:

    def __init__(self) -> None:
        self._room_pack = None

    def with_room_pack(self, value: RoomPack) -> "EscapeRoomGameBuilder":
        self._room_pack = value
        return self

    def build(self) -> EscapeRoomGame:
        if self._room_pack:
            return EscapeRoomGameInteractor(self._room_pack)
        raise ConfigurationError("You must specify a RoomPack")
