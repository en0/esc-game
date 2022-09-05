from unittest import TestCase, skip
from fixtures import a, an

from esc.levels.demo import DemoRoomPack


class DemoRoomPackTests(TestCase):

    def test_room_pack_has_study(self):
        room_pack = DemoRoomPack()
        self.assertIn("Study", room_pack.list_rooms())

