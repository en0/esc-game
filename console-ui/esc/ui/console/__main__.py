from typing import NamedTuple

from .game import EscapeRoomGame
from .prompt import MenuPrompt
from .room_loader import RoomPackLoader


class ConfigOptions(NamedTuple):
    room_pack_namespace: str

    @staticmethod
    def parse():
        return ConfigOptions(
            room_pack_namespace="esc.levels"
        )


def get_room_pack_name(names) -> str:
    if len(names) == 1:
        return names[0]
    menu = MenuPrompt("Select a Room Pack.", "> ", names + ["exit"])
    return menu.prompt()


def main(config: ConfigOptions):
    room_packs = RoomPackLoader(config.room_pack_namespace)
    if not room_packs:
        print("There are no room packs installed. Try installing some!")
        return 1
    choice = get_room_pack_name(room_packs.list_names())
    if choice.lower() != 'exit':
        EscapeRoomGame(room_packs.get_room_pack(choice)).play()


if __name__ == "__main__":
    opts = ConfigOptions.parse()
    main(opts)
