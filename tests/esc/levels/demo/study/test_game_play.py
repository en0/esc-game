from unittest import TestCase, skip
from fixtures import a, an

from esc.core import GameObject
from esc.levels.demo import study


class StudyGamePlayTest(TestCase):

    def test_study_name(self):
        self.assertEqual(study.name, "Study")

    def test_can_build_room(self):
        room = study.creator()
        self.assertIsInstance(room, GameObject)
