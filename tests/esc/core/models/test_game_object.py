from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an

from esc.core import GameObject, InteractionReceiver, Interaction, exceptions


class BasicGameObjectTests(TestCase):

    def test_fixtures_builder_returns_game_object(self):
        game_obj = a.game_object_builder.build()
        self.assertIsInstance(game_obj, GameObject)

    def test_fixtures_builder_with(self):
        builder = a.game_object_builder
        builder.with_name("fixture-name")
        builder.with_details("fixture-details")
        builder.with_summary("fixture-summary")
        builder.with_children([])
        self.assertIsInstance(builder.build(), GameObject)

    def test_fixtures_builder_returns_different_objects(self):
        obj1 = a.game_object_builder.build()
        obj2 = a.game_object_builder.build()
        self.assertIsNot(obj1, obj2)

    def test_get_name_returns_name(self):
        game_obj = a.game_object_builder.with_name("test-name").build()
        self.assertEqual(game_obj.get_name(), "test-name")

    def test_get_details_returns_details(self):
        game_obj = a.game_object_builder.with_details("test-details").build()
        self.assertEqual(game_obj.get_details(), "test-details")

    def test_get_summary_returns_summary(self):
        game_obj = a.game_object_builder.with_summary("test-summary").build()
        self.assertEqual(game_obj.get_summary(), "test-summary")

    def test_children_can_be_none(self):
        game_obj = a.game_object_builder.with_children(None).build()
        self.assertListEqual(game_obj.get_children(), [])

    def test_get_children_returns_children(self):
        children = [
            a.game_object_builder.with_name("child-1").build(),
            a.game_object_builder.with_name("child-2").build(),
            a.game_object_builder.with_name("child-3").build(),
        ]
        game_obj = a.game_object_builder.with_children(children).build()
        self.assertListEqual(game_obj.get_children(), children)

    def test_interaction(self):
        mock_interaction = Mock(spec=Interaction)
        mock_receiver = Mock(spec=InteractionReceiver)
        game_obj = a.game_object_builder.with_name("test-interaction").build()
        game_obj.set_interaction(mock_interaction)
        game_obj.interact(mock_receiver)
        mock_interaction.interact.assert_called_with(mock_receiver)

    def test_interaction_raises_when_not_set(self):
        mock_receiver = Mock(spec=InteractionReceiver)
        game_obj = a.game_object_builder.with_name("test-interaction").build()
        with self.assertRaises(exceptions.NotInteractableError):
            game_obj.interact(mock_receiver)



