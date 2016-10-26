from pathlib import PurePath, Path
from .filewrapbase import FileWrapBase, FileType


class FileWrapLocal(FileWrapBase):
    def __init__(self, uri, type=None):
        super(FileWrapLocal, self).__init__(uri, type)

    def readdir(self):
        if not self.is_dir:
            raise NotADirectoryError
        for path in Path(self.uri).iterdir():
            yield FileWrapLocal(PurePath(self.hostname).joinpath(path).as_posix())

    def mkdir(self, name="", mode=0o777, parents=False, exist_ok=False):
        if not self.is_dir:
            raise NotADirectoryError
        if not name:
            raise ValueError('Name not specified')
        Path(self.uri).joinpath(name).mkdir()

    def rmdir(self, name):
        if not self.is_dir:
            raise NotADirectoryError
        Path(self.uri).rmdir()

    def _map_type(self, val):
        return val

    def _get_type(self):
        p = Path(self.uri)
        ret = FileType.dir if p.is_dir() else \
            FileType.file if p.is_file() else \
            FileType.symlink if p.is_symlink() else \
            None
        if ret:
            return ret
        else:
            raise ValueError('Unknown object type')

    def _get_parent(self):
        return FileWrapLocal(PurePath(self.uri).parent.as_posix())

    def _get_child(self, name):
        for d in self.readdir():
            if d.name == name:
                return d
        raise ValueError('Directory {0} does not have {1} object'.format(self.name, name))
