from pathlib import PurePath
from ftplib import FTP
from .filewrapbase import FileWrapBase, FileType


class FileWrapFtp(FileWrapBase):
    def __init__(self, uri, type=None, username='anonymous', password=''):
        super(FileWrapFtp, self).__init__(uri, type)
        self.username = username
        self.password = password

    def readdir(self):
        if not self.is_dir:
            raise NotADirectoryError
        with FTP(self.hostname, self.username, self.password) as ftp:
            ftp.cwd(self.path)
            for (name, t) in ftp.mlsd(facts=['type']):
                if t['type'] in (FileType.dir.name, FileType.file.name):
                    yield FileWrapFtp(PurePath(self.uri).joinpath(name),
                                      type=t['type'], username=self.username, password=self.password)
                else:
                    continue

    def _map_type(self, val):
        self._ftp_mappings = {
            'dir': FileType.dir,
            'file': FileType.file,
        }
        return self._ftp_mappings[val]

    def _get_type(self):
        """ TODO """
        return self._map_type('dir')

    def _get_parent(self):
        return FileWrapFtp(PurePath(self.uri).parent.as_posix(), username=self.username, password=self.password)
