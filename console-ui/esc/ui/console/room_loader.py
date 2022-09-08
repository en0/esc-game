import inspect
from importlib import import_module
from os import listdir
from typing import Iterator, List

from esc.core.typing import RoomPack


class RoomPackLoader:

    def __init__(self, package_name: str) -> None:
        self._package_name = package_name
        self._loaded_room_packs = []
        self._loaded = {}

    @property
    def _room_packs(self) -> List[RoomPack]:
        if not self._loaded:
            self._load_room_packs()
        return list(self._loaded.values())

    def list_names(self) -> List[str]:
        return [p.get_name() for p in self._room_packs]

    def get_room_pack(self, name: str) -> RoomPack:
        if not self._loaded:
            self._load_room_packs()
        return self._loaded[name.lower()]

    def __bool__(self) -> bool:
        return bool(self._room_packs)

    def __iter__(self) -> Iterator[RoomPack]:
        return iter(self._room_packs)

    def _load_room_packs(self) -> None:
        found_modules = set()
        for module_path in import_module(self._package_name).__path__:
            for submodule_name in listdir(module_path):
                try:
                    pack = import_module(f"{self._package_name}.{submodule_name}")
                    if pack in found_modules:
                        continue
                    found_modules.add(pack)
                    for _, member in inspect.getmembers(pack):
                        if (
                            inspect.isclass(member)
                            and issubclass(member, RoomPack)
                            and not inspect.isabstract(member)
                        ):
                            room_pack = member()
                            self._loaded[room_pack.get_name().lower()] = room_pack
                except ImportError as ex:
                    print(ex)

