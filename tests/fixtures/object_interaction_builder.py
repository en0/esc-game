from .base import BuilderBase
from esc.core.typing import GameObject
from esc.core.interactor.object_interaction import ObjectInteraction
from .basic_game_object_builder import BasicGameObjectBuilder

class ObjectInteractionBuilder(BuilderBase[ObjectInteraction]):

    def __init__(self):
        self._container = BasicGameObjectBuilder().with_name("container").build()

    def with_room_container(self, value: GameObject) -> "ObjectInteractionBuilder":
        self._container = value
        return self

    def with_game_object(self, value: GameObject) -> "ObjectInteractionBuilder":
        self._container.add_child(value)
        return self

    def build(self) -> ObjectInteraction:
        return ObjectInteraction(self._container)
