from esc.core import RoomPackBuilder

from . import study

room_pack = (
    RoomPackBuilder()
     .with_room_container(study.name, study.creator)
     .build()
)

