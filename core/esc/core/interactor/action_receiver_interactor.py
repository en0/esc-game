from typing import Any

from esc.core.typing import GameObject, ActionApi


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

