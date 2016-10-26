from enum import Enum
from pathlib import PurePath


class FileWrapBase(object):
    def __init__(self, uri, type=None):
        def split_uri(uri):
            return (PurePath(uri).parts[0], PurePath(*PurePath(uri).parts[1:]).as_posix())

        self.uri = uri
        self.__type = self._map_type(type) if type else None
        (self.hostname, self.path) = split_uri(uri)
        self.name = PurePath(self.path).name

    def __str__(self):
        return "{0}".format(self.uri)

    def __repr__(self):
        return str(self)

    def readdir(self):
        raise NotImplementedError()

    def mkdir(self, name="", mode=0o777, parents=False, exist_ok=False):
        raise NotImplementedError()

    def rmdir(self, name):
        raise NotImplementedError()

    @property
    def type(self):
        if not self.__type:
            self.__type = self._get_type()
        return self.__type

    @property
    def is_dir(self):
        return self.type == FileType.dir

    @property
    def is_file(self):
        return self.type == FileType.file

    @property
    def is_link(self):
        return self.type == FileType.symlink

    @property
    def parent(self):
        return self._get_parent() if not self.path == '.' else self

    def get_child(self, name):
        try:
            return self._get_child(name)
        except ValueError as e:
            print("Error: {0}".format(e.args))
            return self

    def _map_type(self, val):
        raise NotImplementedError

    def _get_type(self):
        raise NotImplementedError

    def _get_parent(self):
        raise NotImplementedError

    def _get_child(self, name):
        raise NotImplementedError

class FileType(Enum):
    dir = 1
    file = 2
    symlink = 3
