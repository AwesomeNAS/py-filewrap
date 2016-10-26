from pathlib import PurePath
from freenas.dispatcher.client import Client
from .filewrapbase import FileWrapBase, FileType


class FileWrapRemote(FileWrapBase):
    def __init__(self, uri, type=None, username='root', password=''):
        super(FileWrapRemote, self).__init__(uri, type)
        self.client = Client()
        self.username = username
        self.password = password

    def readdir(self):
        if not self.is_dir:
            raise NotADirectoryError
        self.client.connect('ws://'+self.hostname)
        self.client.login_user(self.username, self.password)
        for e in self.client.call_sync('filesystem.list_dir', self.path):
            yield FileWrapRemote(
                PurePath(self.uri).joinpath(e['name']), type=e['type'], username=self.username, password=self.password)

    def _map_type(self, val):
        self._freenas_mappings = {
            'DIRECTORY': FileType.dir,
            'FILE': FileType.file,
        }
        return self._freenas_mappings[val]

    def _get_type(self):
        #self.client.connect('ws://'+self.hostname)
        #self.client.login_user(self.username, self.password)
        """ TODO """
        return self._map_type('DIRECTORY')

    def _get_parent(self):
        return FileWrapRemote(PurePath(self.uri).parent.as_posix(), username=self.username, password=self.password)
