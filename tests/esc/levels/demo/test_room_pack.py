from unittest import TestCase, skip
from fixtures import a, an

from esc.levels.demo import room_pack


class DemoRoomPackTests(TestCase):

    def test_room_pack_has_study(self):
        self.assertIn("Study", room_pack.list_rooms())

