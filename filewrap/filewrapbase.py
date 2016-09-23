from enum import Enum
from pathlib import PurePath


class FileWrapBase(object):
    def __init__(self, uri, type=None):
        def split_uri(uri):
            return (PurePath(uri).parts[0], PurePath(*PurePath(uri).parts[1:]).as_posix())

        self.uri = uri
        self.type = type
        (self.hostname, self.path) = split_uri(uri)

    def readdir(self):
        raise NotImplementedError()

    def mkdir(self, mode=0o777, parents=False, exist_ok=False):
        raise NotImplementedError()

    @property
    def is_dir(self):
        if not self.type:
            self.type = self._get_type()
        return self.type == FileType.dir

    @property
    def is_file(self):
        if not self.type:
            self.type = self._get_type()
        return self.type == FileType.file

    @property
    def is_link(self):
        if not self.type:
            self.type = self._get_type()
        return self.type == FileType.symlink

    @property
    def parent(self):
        return self._get_parent() if not self.path == '.' else self

    def _get_type(self):
        raise NotImplementedError

    def _get_parent(self):
        raise NotImplementedError


class FileType(Enum):
    dir = 1
    file = 2
    symlink = 3
