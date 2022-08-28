from unittest import TestCase, skip
from fixtures import a, an


class DevelopmentEnvTests(TestCase):

    def test_pytest_is_setup(self):
        self.assertTrue(True)
