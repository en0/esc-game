from typing import Callable

from esc.core.builder import GameObjectBuilder
from esc.core.typing import GameObject
from jinja2 import Environment
from yaml import safe_load

from .spec import GameObjectSpec


class YamlGameLoader(Callable[[None], GameObject]):

    def __init__(self, name: str, yaml_path: str):
        self._name = name
        self._yaml_path = yaml_path

    def __call__(self):
        data, constant = self._load_yaml()
        return (
            GameObjectBuilder()
            .with_name(self._name)
            .with_children([
                GameObjectSpec.from_dict(o).build(constant)
                for o in data.get("objects", [])])
            .build()
        )

    def _load_yaml(self):
        env = Environment()
        with open(self._yaml_path) as fd:
            data = safe_load(fd)
            constant = data.get("locals")
            fd.seek(0)
            template = env.from_string(fd.read())
            data = safe_load(template.render(constant))
            return data, constant

