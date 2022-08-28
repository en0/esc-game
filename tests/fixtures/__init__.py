from .game_object_builder import GameObjectBuilder


class _A:
    @property
    def game_object_builder(self) -> GameObjectBuilder:
        return GameObjectBuilder()


class _An:
    ...

a = _A()
an = _An()
