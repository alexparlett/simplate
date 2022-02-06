from unittest import TestCase

import pytest

from simplate.template import Template


class TestTemplate(TestCase):

    def test_render_valid(self):
        under_test = Template()

        ctx = dict(foo="bar")
        template = "{{ pipe( var(foo) | uppercase()) }}"
        result = under_test.render(template, ctx)
        self.assertEqual(result,"BAR")

    def test_render_valid_without_context(self):
        under_test = Template()

        template = "{{ default(foo,bar) }}"
        result = under_test.render(template)
        assert result == "bar"

    def test_render_invalid(self):
        under_test = Template()

        with pytest.raises(Exception) as ex:
            under_test.render(None)
        assert ex.value.args[0] == "template must not be None"

    def test_register_function(self):
        def foo():
            return "bar"

        under_test = Template()

        under_test.register_function("foo", foo)

        template = "{{ foo() }}"
        result = under_test.render(template)
        assert result == "bar"

    def test_register_function_invalid(self):
        def foo():
            return "bar"

        under_test = Template()

        with pytest.raises(Exception) as ex:
            under_test.register_function(None, foo)
        assert ex.value.args[0] == "name can not be None"

        with pytest.raises(Exception) as ex:
            under_test.register_function(1, foo)
        assert ex.value.args[0] == "name must be a str"

        with pytest.raises(Exception) as ex:
            under_test.register_function("name", None)
        assert ex.value.args[0] == "func can not be None"

        with pytest.raises(Exception) as ex:
            under_test.register_function("name", object())
        assert ex.value.args[0] == "func must be a callable"
