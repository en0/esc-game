from esc.core import GameObjectBuilder

from . import const
from .computer import ComputerUseAction
from .door import UseDoorAction


name = "Study"


def creator():

    desk = _create_desk()
    computer = _create_computer()
    bookshelf = _create_bookshelf()

    trash = (
        GameObjectBuilder()
         .with_name("trash")
         .with_alias("trash can")
         .with_alias("waste bin")
         .with_alias("trash bin")
         .with_alias("waste basket")
         .with_alias("waste paper basket")
         .with_inform_action(const.TRASH_INFO, const.INSPECT_ALIASES)
         .build()
    )

    whiteboard = (
        GameObjectBuilder()
         .with_name("whiteboard")
         .with_alias("white board")
         .with_alias("chalk board")
         .with_alias("board")
         .with_inform_action(const.WHITEBOARD_INFO, const.INSPECT_ALIASES)
         .build()
    )

    plant = (
        GameObjectBuilder()
         .with_name("plant")
         .with_alias("house plant")
         .with_inform_action(const.PLANT_INFO, const.INSPECT_ALIASES)
         .with_inform_action(const.PLANT_WATER, ["water"])
         .build()
    )

    door = (
        GameObjectBuilder()
         .with_name("door")
         .with_alias("exit")
         .with_inform_action(const.DOOR_INFO, const.INSPECT_ALIASES, "inspect_msg")
         .with_action(UseDoorAction())
         .with_property("locked", True)
         .build()
    )

    room = (
        GameObjectBuilder()
         .with_name("room")
         .with_alias("study")
         .with_inform_action(const.ROOM_INFO, const.INSPECT_ALIASES)
         .build()
    )

    return (
        GameObjectBuilder()
        .with_name(name)
        .with_child(room)
        .with_child(desk)
        .with_child(computer)
        .with_child(trash)
        .with_child(whiteboard)
        .with_child(plant)
        .with_child(bookshelf)
        .with_child(door)
        .build()
    )


def _create_desk():

    photo = (
        GameObjectBuilder()
         .with_name("photo")
         .with_inform_action(const.PHOTO_INFO, const.INSPECT_ALIASES)
         .build()
    )

    return (
        GameObjectBuilder()
         .with_name("desk")
         .with_alias("table")
         .with_alias("computer desk")
         .with_inform_action(const.DESK_INFO, const.INSPECT_ALIASES)
         .and_with_reveal_decorator()
         .with_child(photo)
         .build()
    )


def _create_bookshelf():

    pma = (
        GameObjectBuilder()
         .with_name("practical malware analysis")
         .with_inform_action(const.PRACTICAL_MALWARE_ANALYSIS_INFO, const.INSPECT_ALIASES)
         .build()
    )

    bhp = (
        GameObjectBuilder()
         .with_name("black hat python")
         .with_inform_action(const.BLACK_HAT_PYTHON_INFO, const.INSPECT_ALIASES)
         .build()
    )

    ls = (
        GameObjectBuilder()
         .with_name("locksport")
         .with_inform_action(const.LOCKSPORT_INFO, const.INSPECT_ALIASES)
         .build()
    )

    ae_box = (
        GameObjectBuilder()
         .with_name("audio engine box")
         .with_alias("audio engine a5+ box")
         .with_inform_action(const.AUDIO_ENGINE_BOX_INFO, const.INSPECT_ALIASES)
         .build()
    )

    ip_box = (
        GameObjectBuilder()
         .with_name("iphone box")
         .with_alias("iphone 13 box")
         .with_alias("iphone 13 pro box")
         .with_alias("iphone 13 pro max box")
         .with_alias("iphone 13 max box")
         .with_inform_action(const.IPHONE_BOX_INFO, const.INSPECT_ALIASES)
         .build()
    )

    yale_box = (
        GameObjectBuilder()
         .with_name("yale box")
         .with_alias("yale lock box")
         .with_inform_action(const.YALE_BOX_INFO, const.INSPECT_ALIASES)
         .build()
    )

    rp_box = (
        GameObjectBuilder()
         .with_name("raspberry pi box")
         .with_alias("raspberry box")
         .with_alias("pi box")
         .with_inform_action(const.RASPBERRY_BOX_INFO, const.INSPECT_ALIASES)
         .build()
    )

    ec_box = (
        GameObjectBuilder()
         .with_name("elite-c box")
         .with_alias("elite c box")
         .with_alias("elite box")
         .with_inform_action(const.ELITE_BOX_INFO, const.INSPECT_ALIASES)
         .build()
    )

    return (
        GameObjectBuilder()
         .with_name("bookshelf")
         .with_alias("book shelf")
         .with_inform_action(const.BOOKSHELF_INFO, const.INSPECT_ALIASES)
         .and_with_reveal_decorator()
         .with_child(pma)
         .with_child(bhp)
         .with_child(ls)
         .with_child(ae_box)
         .with_child(ip_box)
         .with_child(yale_box)
         .with_child(rp_box)
         .with_child(ec_box)
         .build()
    )

def _create_computer():
    return (
        GameObjectBuilder()
         .with_name("computer")
         .with_alias("workstation")
         .with_alias("desktop")
         .with_alias("system")
         .with_alias("machine")
         .with_inform_action(const.COMPUTER_INFO, const.INSPECT_ALIASES)
         .with_action(ComputerUseAction())
         .build()
    )
