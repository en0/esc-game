from unittest import TestCase, skip
from fixtures import a, an

from esc.core import Room, NotFoundError


class BasicRoomTests(TestCase):

    def test_fixtures_builder_returns_room(self):
        room = a.basic_room_builder.build()
        self.assertIsInstance(room, Room)

    def test_fixtures_builder_with(self):
        builder = a.basic_room_builder
        builder.with_name("fixture-name")
        self.assertIsInstance(builder.build(), Room)

    def test_get_name_returns_name(self):
        room = a.basic_room_builder.with_name("test-name").build()
        self.assertEqual(room.get_name(), "test-name")

    def test_list_object_names(self):
        room = a.basic_room_builder.build()
        objs = [
            a.basic_game_object_builder.with_name("obj-1").build(),
            a.basic_game_object_builder.with_name("obj-2").build(),
            a.basic_game_object_builder.with_name("obj-3").build(),
        ]

        self._add_objs(room, objs)

        self.assertListEqual(room.list_object_names(), [o.get_name() for o in objs])

    def test_get_object(self):
        room = a.basic_room_builder.build()
        objs = [
            a.basic_game_object_builder.with_name("obj-1").build(),
            a.basic_game_object_builder.with_name("obj-2").build(),
            a.basic_game_object_builder.with_name("obj-3").build(),
        ]

        self._add_objs(room, objs)

        for o in objs:
            self.assertIs(room.get_game_object(o.get_name()), o)

    def test_get_object_raises_not_found(self):
        room = a.basic_room_builder.build()
        with self.assertRaises(NotFoundError):
            room.get_game_object("no-exist")

    def test_summarize(self):
        room = a.basic_room_builder.with_name("test-room").build()
        objs = [
            a.basic_game_object_builder.with_name("obj-1").with_summary("To your foo you see a bar.").build(),
            a.basic_game_object_builder.with_name("obj-2").with_summary("To your baz you see a quz.").build(),
        ]

        self._add_objs(room, objs)
        self.assertEqual(
            room.get_summary(),
            "To your foo you see a bar. To your baz you see a quz."
        )

    def _add_objs(self, room, objs) -> None:
        for o in objs:
            room.add_game_object(o)

