from unittest import TestCase, skip
from unittest.mock import Mock
from fixtures import a, an


class DelegateCommandTests(TestCase):
    def test_delegate_called_without_args(self):
        delegate_mock = Mock()
        a.delegate_command_builder.with_delegate(delegate_mock).build().execute()
        delegate_mock.assert_called_with()

    def test_delegate_called_with_args(self):
        delegate_mock = Mock()
        a.delegate_command_builder.with_delegate(delegate_mock).with_args("foo", "bar").build().execute()
        delegate_mock.assert_called_with("foo", "bar")

    def test_delegate_called_with_kargs(self):
        delegate_mock = Mock()
        a.delegate_command_builder.with_delegate(delegate_mock).with_kwargs(foo="bar", baz="quz").build().execute()
        delegate_mock.assert_called_with(foo="bar", baz="quz")

    def test_delegate_called_with_args_and_kargs(self):
        delegate_mock = Mock()
        a.delegate_command_builder.with_delegate(delegate_mock).with_args("foo", "bar").with_kwargs(foo="bar", baz="quz").build().execute()
        delegate_mock.assert_called_with("foo", "bar", foo="bar", baz="quz")

    def test_delegate_called_twice(self):
        delegate_mock = Mock()
        command = a.delegate_command_builder.with_delegate(delegate_mock).with_args("foo", "bar").with_kwargs(foo="bar", baz="quz").build()

        command.execute()
        delegate_mock.assert_called_with("foo", "bar", foo="bar", baz="quz")

        delegate_mock.reset_mock()

        command.execute()
        delegate_mock.assert_called_with("foo", "bar", foo="bar", baz="quz")
