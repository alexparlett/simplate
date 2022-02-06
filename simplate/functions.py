import typing
from functools import reduce


def lowercase(_, target: typing.AnyStr):
    """
    lowercase is meant to be used with pipe as it takes the current context and lowercase it

    Signature is a bit of a hack due to assumptions made of how pipe works
    """
    return target.lower()


def uppercase(_, target: typing.AnyStr):
    """
    uppercase is meant to be used with pipe as it takes the current context and uppercase it

    Signature is a bit of a hack due to assumptions made of how pipe works
    """
    return target.upper()


def join(separator: typing.AnyStr, ctx: typing.Any):
    """
    join is meant to be used with pipe as it takes the current context and joins whatever that may be
    """
    return separator.strip().join(iter(ctx))


def pipe(target: typing.AnyStr, ctx: typing.Any, template):
    """
    pipe calls a set of functions in order, taking the result of the previous and applying it to the next

    Nested pipes won't work because of the naive split
    """
    parts = target.split("|")
    result = ctx
    for part in parts:
        function, arguments = template.find_function(part)
        result = template.execute_function_with_maximum_arity(function, arguments, result)
    return result


def maps(target: typing.AnyStr, ctx: typing.Any, template):
    """
    maps an var, transforming it by a sub template with an optional separator
    """
    args = target.split(",", 1)
    if len(args) != 2:
        raise Exception("map must have two arguments, a variable and a template split by a ,")

    var_path = args[0]
    sub_template = args[1]

    found = get_var_from_path(var_path, ctx)
    if not found:
        raise Exception("no matching var " + var_path)
    return list(map(lambda x: template.render(sub_template, dict(current=x)), iter(found)))


def var(target: typing.AnyStr, ctx: typing.Any):
    """
    var works by looking up the target in the ctx
    """
    if target == "this":
        return ctx
    found = get_var_from_path(target, ctx)
    if not found:
        raise Exception("no matching var " + target)
    return found


def default(target: typing.AnyStr, ctx: typing.Any):
    """
    default works by having n number of variables to look up and the last element being a default.
    e.g. default( foo , bar ) => would default to bar if foo is not in the ctx.
    """
    # We must have at least two items
    items = target.split(",")
    if len(items) < 2:
        raise Exception("default must have at least two arguments, a variable and a default split by a ,")

    # Do this in a for loop so we don't evaluate unnecessarily
    for item in items[:-1]:
        found = get_var_from_path(item, ctx)
        if found:
            return found

    # Return default if none found
    return items[-1]


def get_var(parent: typing.Any, var_name: typing.AnyStr):
    """
    get a variable from the its parent
    """
    return parent.get(var_name)


def get_var_from_path(var_path: typing.AnyStr, ctx: typing.Any):
    """
    use a declarative syntax to traverse complex objects
    i.e. in { foo: { bar: cat }}, foo.bar => cat
    """
    path = var_path.split(".")
    return reduce(get_var, path, ctx)
