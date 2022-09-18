from typing import NamedTuple
from esc.core.typing import Interaction, InteractionResponse, InteractionResponseType, RoomPack, EscapeRoomGame
from esc.core.builder import EscapeRoomGameBuilder

from .game import Game
from .prompt import MenuPrompt, BasicGamePrompt
from .room_loader import RoomPackLoader


class ConfigOptions(NamedTuple):
    room_pack_namespace: str

    @staticmethod
    def parse():
        return ConfigOptions(
            room_pack_namespace="esc.levels"
        )

def main(config: ConfigOptions):

    prompt = BasicGamePrompt()
    room_packs = RoomPackLoader(config.room_pack_namespace)

    if not room_packs:
        print("There are no room packs installed. Try installing some!")
        return 1

    room_choice = prompt.prompt_with_choices("Select a Room Pack.", room_packs.list_names())
    room_pack = room_packs.get_room_pack(room_choice)

    Game(
        room_pack=room_pack,
        prompt=prompt,
        game=(
            EscapeRoomGameBuilder()
            .with_room_pack(room_pack)
            .build()
        )
    ).play()


if __name__ == "__main__":
    opts = ConfigOptions.parse()
    main(opts)
