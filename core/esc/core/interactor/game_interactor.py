from typing import Dict, List

from esc.core.typing import EscapeRoomGame, Interaction, RoomPack

from .object_interaction import ObjectInteraction


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
        interaction = ObjectInteraction(self._room_container)
        interaction.set_target(object_name)
        interaction.set_action(action_name)
        if using_object:
            interaction.set_using(using_object)
        return iter(interaction)
