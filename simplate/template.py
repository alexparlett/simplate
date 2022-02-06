import inspect
import re
import typing
from functools import partial

import simplate.functions as funcs


class Template:
    _template_pattern = re.compile("\\{\\{(.+?)\\}\\}")
    _function_pattern = re.compile("([a-zA-Z]+)\\((.*)\\)")
    _functions = dict()

    def __init__(self):
        self.register_function("var", funcs.var)
        self.register_function("default", funcs.default)
        self.register_function("map", funcs.maps)
        self.register_function("pipe", funcs.pipe)
        self.register_function("join", funcs.join)
        self.register_function("uppercase", funcs.uppercase)
        self.register_function("lowercase", funcs.lowercase)

    def register_function(self, name: typing.AnyStr, func: typing.Callable):
        """
        Register a new function to make it available in the template
        """
        if name is None:
            raise Exception("name can not be None")
        if not isinstance(name, str):
            raise Exception("name must be a str")
        if func is None:
            raise Exception("func can not be None")
        if not isinstance(func, typing.Callable):
            raise Exception("func must be a callable")
        self._functions[name] = func

    def render(self, template: typing.AnyStr, ctx: typing.Dict = dict()) -> typing.AnyStr:
        """
        Render a template with an optionally provided context
        """
        if not template:
            raise Exception("template must not be None")

        return re.sub(pattern=self._template_pattern,
                      repl=partial(self.replace_match, ctx),
                      string=template)

    def replace_match(self, ctx: typing.Any, match: typing.Match) -> typing.AnyStr:
        """
        Perform replacement on match.

        Note: this is using a separate regex template instead of one (which we could do) so that we can give better
        error messages.
        """

        function, arguments = self.find_function(match.group())

        return self.execute_function_with_maximum_arity(function, arguments, ctx)

    def find_function(self, element):
        """
        find a matching function, extract its arguments
        """
        found = re.search(self._function_pattern, element)
        if not found:
            raise Exception("invalid operation syntax (" + element + ")")
        function_name = found.group(1).strip()
        function = self._functions.get(function_name)
        if not function:
            raise Exception("invalid operation name " + function_name)
        arguments = found.group(2).strip()
        return function, arguments

    def execute_function_with_maximum_arity(self, function: typing.Callable, target: typing.AnyStr, ctx: typing.Any):
        """
        Execute the found function with the maximum number of arguments
        """
        # find the number of arguments excluding self
        signature = inspect.signature(function)
        args = len(signature.parameters)
        # execute
        if args == 0:
            return function()
        elif args == 1:
            return function(target)
        elif args == 2:
            return function(target, ctx)
        elif args == 3:
            return function(target, ctx, self)
        else:
            raise Exception("function must have a signature of () | (match) | (match,ctx) | (match,ctx,template)")
