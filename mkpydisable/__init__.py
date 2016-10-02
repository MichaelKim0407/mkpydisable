__author__ = 'Michael'


def cleanup(globals, locals):
    for key in globals.keys():
        globals.pop(key)
    for key in locals.keys():
        locals.pop(key)


from . import builtins
from . import open
