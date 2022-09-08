from unittest import TestCase

from esc.levels.demo import DemoRoomPack


class DemoRoomPackTests(TestCase):

    def test_room_pack_has_study(self):
        room_pack = DemoRoomPack()
        self.assertIn("Study", room_pack.list_rooms())

