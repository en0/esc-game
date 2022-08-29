from unittest import TestCase, skip
from fixtures import a, an


class GameInteractorTests(TestCase):

    @skip("working on loader first")
    def test_list_room_names(self):
        names = ["foo", "bar", "baz"]
        game = a.game_interactor_builder.build()
        self.assertListEqual(game.list_room_names(), names)
