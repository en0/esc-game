from typing import List, Dict, Set, Any, Iterator
from .domain import (
    ActionApi,
    ActionError,
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
        using_object_name = (
            self._room_container.get_child(using_object).get_name()
            if using_object else None
        )
        generator = action.trigger(receiver, using_object_name)
        return ActionInteractor(generator, object_name, action_name)


class ActionInteractor(Interaction):

    def __init__(
        self,
        generator: InteractionResponseGenerator,
        object_name: str,
        action_name: str,
    ) -> None:
        self._gen = generator
        self._current = None
        self._object_name = object_name
        self._action_name = action_name
        self._input = None

    def __iter__(self) -> Iterator[Interaction]:
        return self

    def __next__(self) -> Interaction:
        if self._current is None:
            self._set_current()
        elif self._current.get_type() == InteractionResponseType.DONE:
            raise StopIteration()
        elif self._current.get_type() == InteractionResponseType.COLLECT_INPUT:
            self._set_current_and_send()
        else:
            self._set_current()
        self._input = None
        return self

    def _set_current(self):
        try:
            self._current = next(self._gen)
        except StopIteration:
            raise
        except Exception as ex:
            raise ActionError(self._object_name, self._action_name) from ex

    def _set_current_and_send(self):
        try:
            self._current = self._gen.send(self._input)
        except StopIteration:
            raise
        except Exception as ex:
            raise ActionError(self._object_name, self._action_name) from ex

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

    def reveal_all_child_objects(self, object_name: str) -> None:
        obj = self._container.get_child(object_name)
        for child in obj.get_children():
            self._container.add_child(child)

