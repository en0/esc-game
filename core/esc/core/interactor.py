from typing import List, Dict, Set, Any, Iterator
from .domain import (
    ActionApi,
    EscapeRoomGame,
    GameObject,
    Interaction,
    InteractionResponseGenerator,
    InteractionResponseType,
    RoomPack,
)


class EscapeRoomGameInteractor(EscapeRoomGame):

    def __init__(self, room_pack: RoomPack) -> None:
        self._room_pack = room_pack
        self._room_container = None

    def load_room(self, name: str) -> List[str]:
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
        generator = action.trigger(receiver)
        return ActionInteractor(generator)


class ActionInteractor(Interaction):

    def __init__(self, generator: InteractionResponseGenerator) -> None:
        self._gen = generator
        self._current = None
        self._input = None

    def __iter__(self) -> Iterator[Interaction]:
        return self

    def __next__(self) -> Interaction:
        if self._current is None:
            self._current = next(self._gen)
        elif self._current.get_type() == InteractionResponseType.DONE:
            raise StopIteration()
        elif self._current.get_type() == InteractionResponseType.COLLECT_INPUT:
            self._current = self._gen.send(self._input)
        else:
            self._current = next(self._gen)
        self._input = None
        return self

    def inform_input(self, value: str) -> None:
        self._input = value

    def get_type(self) -> InteractionResponseType:
        return self._current.get_type()

    def get_message(self) -> str:
        return self._current.get_message()

    def get_hits(self) -> Set[str]:
        return self._current.get_hits()


class ActionReceiverInteractor(ActionApi):

    def __init__(self, room: GameObject, sender: GameObject) -> None:
        self._container = room
        self._sender_name = sender.get_name()

    def get_owner_name(self) -> str:
        return self._sender_name

    def set_object_property(self, object_name: str, key: str, value: Any) -> None:
        obj = self._container.get_child(object_name)
        obj.set_property(key, value)

    def get_object_property(self, object_name: str, key: str) -> None:
        obj = self._container.get_child(object_name)
        return obj.get_property(key)

    def reveal_child_object(self, object_name: str, child_name: str) -> None:
        obj = self._container.get_child(object_name)
        new_obj = obj.get_child(child_name)
        self._container.add_child(new_obj)

