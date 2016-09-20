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

    @property
    def is_dir(self):
        if not self.type:
            self.type = self._get_type()
        return self.type == 'dir'

    @property
    def is_file(self):
        if not self.type:
            self.type = self._get_type()
        return self.type == 'file'

    @property
    def is_link(self):
        if not self.type:
            self.type = self._get_type()
        return self.type == 'symlink'

    @property
    def parent(self):
        return self._get_parent() if not self.path == '.' else self

    def _get_type(self):
        raise NotImplementedError

    def _get_parent(self):
        raise NotImplementedError
