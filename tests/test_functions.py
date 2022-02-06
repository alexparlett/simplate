from unittest import TestCase

import pytest as pytest

from simplate.functions import default, var, maps, join, pipe, uppercase, lowercase
from simplate.template import Template


class Test(TestCase):
    def test_default_valid(self):
        ctx = dict(foo="bar")
        assert default("foo,oops", ctx) == "bar"
        assert default("cat,foo,oops", ctx) == "bar"
        assert default("cat,oops", ctx) == "oops"

    def test_default_invalid(self):
        ctx = dict()

        with pytest.raises(Exception) as ex:
            default("", ctx)
        assert ex.value.args[0] == "default must have at least two arguments, a variable and a default split by a ,"

        with pytest.raises(Exception) as ex:
            default("foo", ctx)
        assert ex.value.args[0] == "default must have at least two arguments, a variable and a default split by a ,"

    def test_var_valid(self):
        ctx = dict(foo="bar", bar=dict(foo="cat"))
        assert var("foo", ctx) == "bar"
        assert var("bar.foo", ctx) == "cat"

    def test_var_invalid(self):
        ctx = dict(foo="bar", bar=dict(foo="cat"))
        with pytest.raises(Exception) as ex:
            var("cat", ctx)
        assert ex.value.args[0] == "no matching var cat"

    def test_map_valid(self):
        ctx = dict(foo=["bar", "cat"])
        template = Template()
        assert maps("foo,{{ var(current) }}", ctx, template) == ["bar", "cat"]
        assert maps("foo,bad template", ctx, template) == ["bad template", "bad template"]

    def test_map_invalid(self):
        ctx = dict(foo=["bar", "cat"])
        template = Template()

        with pytest.raises(Exception) as ex:
            maps("bar", ctx, template)
        assert ex.value.args[0] == "map must have two arguments, a variable and a template split by a ,"

        with pytest.raises(Exception) as ex:
            maps("bar,{{ var(this) }}", ctx, template)
        assert ex.value.args[0] == "no matching var bar"

        with pytest.raises(Exception) as ex:
            maps("foo,{{ fak }}", ctx, template)
        assert ex.value.args[0] == "invalid operation syntax ({{ fak }})"

    def test_join(self):
        ctx = ["bar", "cat"]

        assert join(",", ctx) == "bar,cat"

    def test_pipe(self):
        ctx = dict(foo=["bar", "cat"])
        template = Template()

        assert pipe(" var(foo) | join(,) ", ctx, template) == "bar,cat"

    def test_uppercase(self):
        ctx = "bar"

        assert uppercase(ctx) == "BAR"

    def test_lowercase(self):
        ctx = "BAR"

        assert lowercase(ctx) == "bar"
