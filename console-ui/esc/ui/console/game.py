from textwrap import wrap
from typing import Callable
from esc.core import RoomPack, EscapeRoomGameBuilder, Interaction, InteractionResponse, InteractionResponseType, ObjectNotFoundError, ActionNotFoundError

from .prompt import HistoryPromptSession, MenuPrompt


class EscapeRoomGame:

    def __init__(self, room_pack: RoomPack):
        self._playing = False
        self._room_pack = room_pack
        self._room_name = None
        self._room_menu = MenuPrompt(
            "What room do you want to play?", "> ",
            room_pack.list_rooms())
        self._game_prompt = HistoryPromptSession(
            r"(\w*)\s?(.*)",
            error_message="Try help to see options",
            prompt_color="#009999"
        )
        self._interactive_prompt = HistoryPromptSession()
        self._simple_prompt = HistoryPromptSession()
        self._game = (
            EscapeRoomGameBuilder()
             .with_room_pack(room_pack)
             .build())

    def play(self):
        self._load_room()
        self._play()

    def _load_room(self) -> None:
        rooms = self._room_pack.list_rooms()
        if len(rooms) == 1:
            self._room_name = rooms[0]
        else:
            self._room_name = self._room_menu.prompt()
        self._game.load_room(self._room_name)

    def _play(self):
        self._playing = True
        self._handle_interaction(self._game.interact("room", "inspect"))
        while self._playing:
            cmd, args = self._game_prompt.prompt(f"{self._room_name}> ")
            cmd, args = cmd.lower(), args.lower()
            if cmd == "help":
                self._show_help()
            elif cmd in ["exit", "quit"]:
                self._playing = False
            else:
                self._take_turn(cmd, args)

    def _take_turn(self, cmd, args):
        try:
            result = self._game.interact(args, cmd)
            self._handle_interaction(result)

        except ObjectNotFoundError:
            self._print(f"!! What do you want to [{cmd}]?")

        except ActionNotFoundError:
            self._print(f"!! I don't know how to do that to [{args}]")

    def _handle_interaction(self, interaction: Interaction):
        for response in interaction:
            handler = self._get_handler(response)
            handler(response)

    def _get_handler(self, response: InteractionResponse) -> Callable[[Interaction], None]:
        return {
            InteractionResponseType.COLLECT_INPUT: self._collect_input_handler,
            InteractionResponseType.INFORM_RESULT: self._inform_result_handler,
            InteractionResponseType.INFORM_WIN: self._inform_end_game_handler,
            InteractionResponseType.INFORM_LOSE: self._inform_end_game_handler,
            InteractionResponseType.DONE: lambda x: 0
        }[response.get_type()]

    def _collect_input_handler(self, response: Interaction) -> None:
        hidden = "hidden" in response.get_hits()
        if "interactive" in response.get_hits():
            value = self._interactive_prompt.prompt(response.get_message(), hidden)
        else:
            value = self._simple_prompt.prompt(response.get_message(), hidden)
        response.inform_input(value)

    def _inform_result_handler(self, response: Interaction) -> None:
        if "interactive" in response.get_hits():
            self._print(response.get_message())
        else:
            self._print("")
            self._print(response.get_message())
            self._print("")

    def _inform_end_game_handler(self, response: Interaction) -> None:
        self._print("")
        self._print(response.get_message())
        self._print("")
        self._playing = False

    def _show_help(self):
        self._print("")
        self._print("Type commands to play the game.")
        self._print("Some examples are:\n")
        self._print(f"  {self._room_name}> inspect room")
        self._print(f"  {self._room_name}> open door")
        self._print("")
        self._print("There are many more options. You will have to use your imagination.")
        self._print("")

    def _print(self, text: str) -> None:
        print("\n".join(wrap(text)))
