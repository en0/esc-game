from typing import Dict, List

from esc.core.typing import EscapeRoomGame, Interaction, RoomPack

from .action_interactor import ActionInteractor
from .action_receiver_interactor import ActionReceiverInteractor


class EscapeRoomGameInteractor(EscapeRoomGame):

    def __init__(self, room_pack: RoomPack) -> None:
        self._room_pack = room_pack
        self._room_container = None

    def load_room(self, name: str) -> None:
        self._room_container = self._room_pack.create_room(name)

    def get_object_actions(self) -> Dict[str, List[str]]:
        return {
            k.get_name(): k.list_actions()
            for k in self._room_container.get_children()
        }

    def interact(
            self,
            object_name: str,
            action_name: str,
            using_object: str = None,
    ) -> Interaction:
        game_object = self._room_container.get_child(object_name)
        action = game_object.get_action(action_name)
        receiver = ActionReceiverInteractor(self._room_container, game_object)
        using_object_name = (
            self._room_container.get_child(using_object).get_name()
            if using_object else None
        )
        generator = action.trigger(receiver, using_object_name)
        return ActionInteractor(generator, object_name, action_name)
