from pathlib import PurePath, Path
from .filewrapbase import FileWrapBase


class FileWrapLocal(FileWrapBase):
    def __init__(self, uri, type=None):
        super(FileWrapLocal, self).__init__(uri, type)

    def readdir(self):
        if not self.is_dir:
            raise NotADirectoryError
        for path in Path(self.uri).iterdir():
            yield FileWrapLocal(PurePath(self.hostname).joinpath(path).as_posix())

    def _get_type(self):
        p = Path(self.uri)
        ret = 'dir' if p.is_dir() else 'file' if p.is_file() else  'symlink' if p.is_symlink() else None
        if ret:
            return ret
        else:
            raise ValueError('Unknown object type')

    def _get_parent(self):
        return FileWrapLocal(PurePath(self.uri).parent.as_posix())
