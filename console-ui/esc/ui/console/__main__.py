from typing import NamedTuple

from .game import EscapeRoomGame
from .loader import RoomPackLoader
from .prompt import MenuPrompt


class CmdOpts(NamedTuple):
    room_pack_namespace: str

    @staticmethod
    def parse():
        return CmdOpts(
            room_pack_namespace="esc.levels"
        )


def get_room_pack_name(names) -> str:
    if len(names) == 1:
        return names[0]
    menu = MenuPrompt("Select a Room Pack.", "> ", names + ["exit"])
    return menu.prompt()


def main(opts: CmdOpts):
    room_packs = RoomPackLoader(opts.room_pack_namespace)
    if not room_packs:
        print("There are no room packs installed. Try installing some!")
        return 1
    choice = get_room_pack_name(room_packs.list_names())
    if choice.lower() != 'exit':
        EscapeRoomGame(room_packs.get_room_pack(choice)).play()

if __name__ == "__main__":
    opts = CmdOpts.parse()
    main(opts)
