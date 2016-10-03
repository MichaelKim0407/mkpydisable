import __builtin__
import os

from mklibpy.common.string import String, StringCollection

__author__ = 'Michael'

__open__ = __builtin__.open
__abspath__ = os.path.abspath
__exists__ = os.path.exists


class AccessDenied(Exception):
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

    def __str__(self):
        return "Access to file \'{}\' with mode \'{}\' is denied".format(self.name, self.mode)


class AllowPolicy(object):
    NONE = 0
    ALL = 256
    FILES = 1
    DIRS = 2
    EXTENSIONS = 4
    DIRS_AND_EXTENSIONS = 8

    def __init__(self, value=0):
        self.__value = value
        self.__all = False
        self.__files = StringCollection()
        self.__dirs = StringCollection()
        self.__exts = StringCollection()

    def add_files(self, *files):
        self.__files.add(*[__abspath__(f) for f in files])

    def add_dirs(self, *dirs):
        self.__dirs.add(*[__abspath__(f) for f in dirs])

    def add_extensions(self, *extensions):
        self.__exts.add(*extensions)

    def allows(self, name):
        if self.__value == AllowPolicy.NONE:
            return False
        elif self.__value & AllowPolicy.ALL:
            return True

        if self.__value & AllowPolicy.FILES:
            if name == self.__files:
                return True
        if self.__value & AllowPolicy.DIRS:
            if name.startswith(self.__dirs):
                return True
        if self.__value & AllowPolicy.EXTENSIONS:
            if name.endswith(self.__exts):
                return True
        if self.__value & AllowPolicy.DIRS_AND_EXTENSIONS:
            if name.startswith(self.__dirs) and name.endswith(self.__exts):
                return True

        return False


class LimitedOpen(object):
    def __init__(self):
        self.__r = AllowPolicy()
        self.__w = AllowPolicy()
        self.__a = AllowPolicy()
        self.__wo = False

    def set_read_policy(self, p):
        self.__r = p

    def set_write_policy(self, p):
        self.__w = p

    def set_append_policy(self, p):
        self.__a = p

    def allow_write_override(self, allow=True):
        self.__wo = allow

    def make(self):
        def __new_open(name, mode='r', *args, **kwargs):
            abs_name = String(os.path.abspath(name))

            def __builtin__call():
                return __open__(abs_name, mode=mode, *args, **kwargs)

            def __raise():
                raise AccessDenied(name, mode)

            if "r" in mode:
                if self.__r.allows(abs_name):
                    return __builtin__call()
                else:
                    __raise()
            elif "w" in mode:
                if (not self.__wo) and __exists__(abs_name):
                    __raise()
                if self.__w.allows(abs_name):
                    return __builtin__call()
                else:
                    __raise()
            elif "a" in mode:
                if self.__a.allows(abs_name):
                    return __builtin__call()
                else:
                    __raise()
            else:
                __raise()

        return __new_open
