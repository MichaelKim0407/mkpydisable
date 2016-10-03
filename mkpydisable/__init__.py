__author__ = 'Michael'


def cleanup(globals, locals, *exceptions):
    for key in globals.keys():
        if globals[key] in exceptions:
            continue
        globals.pop(key)
    for key in locals.keys():
        if locals[key] in exceptions:
            continue
        locals.pop(key)


from . import builtins
from . import import_
from . import open
