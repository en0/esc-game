from collections import deque
from os import path
from typing import Deque, Dict, List, Optional

from esc.core.action import (CollectInputInteractionResponse, CompleteInteractionResponse,
                             InformResultInteractionResponse)
from esc.core.typing import Action, ActionApi, InteractionResponseGenerator


def inform(msg):
    return InformResultInteractionResponse(msg, {"interactive"})


def collect(msg):
    return CollectInputInteractionResponse(msg, {"interactive"})


def collect_hidden(msg):
    return CollectInputInteractionResponse(msg, {"interactive", "hidden"})


class StudyComputerUseAction(Action):

    def __init__(self, constant: Dict):
        self._name = constant["COMPUTER_USE_ALIASES"][0]
        self._aliases = constant["COMPUTER_USE_ALIASES"][1:]
        self._hostname = f"{constant['COMPUTER_USERNAME']}_pc"
        self._username = constant["COMPUTER_USERNAME"]
        self._passwords = constant["COMPUTER_PASSWORDS"]
        self._motd = constant["COMPUTER_MOTD"]
        self._mqtt_password = constant["MQTT_PASSWORD"]
        self._mqtt_topic = constant["MQTT_TOPIC"]
        self._door_info_unlocked = constant["DOOR_INFO_UNLOCKED"]
        self._fs = {
            "/": "bin home",
            "/bin": "echo id ls man whoami send_mqtt",
            "/home": self._username,
            f"/home/{self._username}": "",
        }
        self._pwd: str = None
        self._history: Deque[str] = None
        self._cmdline: str = None
        self._cmd: str = None
        self._args: List[str] = None
        self._opts: Dict[str, str] = None
        self._raw_args: List[str] = None
        self._api = None

    @property
    def _prompt(self):
        return f"{self._username}@{self._hostname}:{self._pwd}$ "

    def get_name(self) -> str:
        return self._name

    def get_aliases(self) -> List[str]:
        return self._aliases

    def trigger(
        self,
        api: ActionApi,
        using_object: Optional[str],
    ) -> InteractionResponseGenerator:
        self._api = api
        yield from self._banner()
        yield from self._login()
        yield from self._show_motd()
        yield from self._bash()
        yield CompleteInteractionResponse()

    def _banner(self):
        yield inform("Light Weight 1.0")

    def _login(self):
        success = False
        for _ in range(3):
            username = yield collect(f"{self._hostname} login: ")
            password = yield collect_hidden("password: ")
            if username == self._username and password in self._passwords:
                success = True
                break
            yield inform("Incorrect login!")

        if not success:
            yield inform("Too many failed login attempts... Abort!")
            yield CompleteInteractionResponse()

    def _show_motd(self):
        yield inform(self._motd)

    def _bash(self):
        self._history = deque(maxlen=50)
        self._history.append("send_mqtt -h mqtt.local -t study/light -m on")
        self._pwd = f"/home/{self._username}"
        while True:
            self._cmdline = yield collect(self._prompt)
            self._parse_cmdline()
            yield from self._execve()

    def _parse_cmdline(self):
        self._cmd, *self._raw_args = self._cmdline.split(" ")
        self._args = []
        self._opts = {}

        iter_args = iter(self._raw_args)
        while True:
            try:
                key = next(iter_args)
                if not key.startswith('-'):
                    self._args.append(key)
                else:
                    self._opts[key] = next(iter_args)
            except StopIteration:
                break

    def _execve(self):
        def with_history(fn):
            def _wrap():
                self._history.append(self._cmdline)
                yield from fn()
            return _wrap

        yield from {
            "cd": self._do_cd,
            "echo": with_history(self._do_echo),
            "exit": self._do_exit,
            "help": self._do_help,
            "history": self._do_history,
            "id": with_history(self._do_id),
            "ls": with_history(self._do_ls),
            "man": with_history(self._do_man),
            "pwd": self._do_pwd,
            "whoami": with_history(self._do_whoami),
            "send_mqtt": with_history(self._do_send_mqtt),
        }.get(self._cmd, self._do_not_implemented)()

    def _do_cd(self):
        p = path.abspath(self._args[0] if self._args else self._pwd)
        if p in self._fs:
            self._pwd = p
        else:
            yield inform("cd: No such directory.")

    def _do_echo(self):
        yield inform(" ".join(self._raw_args))

    def _do_exit(self):
        yield inform("Session closed by user.")
        yield CompleteInteractionResponse()

    def _do_help(self):
        yield inform(
            "LightWeight bash, version 0.1\n"
            "These shell commands are defined internally. Type 'help' to see list.\n"
            "Use 'man [COMMAND] to find out more about commands not in this list.\n"
            "\n"
            "cd       Change the current working directory. Full path name required.\n"
            "exit     Exit the shell.\n"
            "help     Display information about builtin commands\n"
            "history  Display the history list.\n"
            "pwd      Display the current working directory.\n"
        )

    def _do_history(self):
        for cmd in self._history:
            yield inform(cmd)

    def _do_id(self):
        yield inform(f"uid=1000({self._username}) gid=1000({self._username}) groups=1000({self._username}),4(adm)")

    def _do_ls(self):
        for p in [self._pwd] if not self._args else self._args:
            result = self._fs.get(path.normpath(p))
            if result is None:
                yield inform("ls: No such file or directory")
                break;
            else:
                yield inform(result)

    def _do_man(self):
        if not self._args:
            yield inform("What manual page do you want?")
        else:
            man = {
                "echo": "echo - Display a line of text\nUSAGE: echo STRING\n",
                "id": "id - Print real and effective user and group IDs\nUSAGE: id\n",
                "ls": "ls - List directory contents\nFull pathname must be given\nUSAGE: ls ABS_PATH\n",
                "man": "man - An interface to the system reference manuals.\nUSAGE: man PAGE\n",
                "whoami": "whoami - Print the effective user name.\nUSAGE: whoami",
                "send_mqtt": (
                    "send_mqtt - Publish a message to an MQTT topic.\n"
                    "USAGE: send_mqtt [-h host] [-u username] [-p password] [-t topic] [-m message]\n"
                ),
            }.get(self._args[0])
            yield inform(man)

    def _do_pwd(self):
        yield inform(self._pwd)

    def _do_whoami(self):
        yield inform(self._username)

    def _do_not_implemented(self):
        yield inform("Command not implemented.")

    def _do_send_mqtt(self):
        if not all([k in self._opts for k in ["-h", "-t", "-m"]]):
            yield inform("send_mqtt: Input error. Check manual.")
        elif self._opts["-h"] != "mqtt.local":
            yield inform("send_mqtt: Host unreachable.")
        elif "-u" not in self._opts or "-p" not in self._opts:
            yield inform("send_mqtt: Connection Refused: not authorized.")
        elif self._opts["-u"] not in self._username:
            yield inform("send_mqtt: Connection Refused: not authorized.")
        elif self._opts["-p"] != self._mqtt_password:
            yield inform("send_mqtt: Connection Refused: not authorized.")
        elif self._opts["-t"].lower() == self._mqtt_topic and self._opts["-m"].lower() == "unlock":
            self._api.set_object_property("door", "inspect_msg", self._door_info_unlocked)
            self._api.set_object_property("door", "locked", False)
            yield inform("Message Sent")
        else:
            yield inform("Message Sent")

