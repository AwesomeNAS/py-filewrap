from pathlib import PurePath
from freenas.dispatcher.client import Client
from .filewrapbase import FileWrapBase


class FileWrapRemote(FileWrapBase):
    def __init__(self, uri, type=None, user='root', password=''):
        super(FileWrapRemote, self).__init__(uri, type)
        self.client = Client()
        self.user = user
        self.password = password

    def readdir(self):
        if not self.is_dir:
            raise NotADirectoryError
        self.client.connect('ws://'+self.hostname)
        self.client.login_user(self.user, self.password)
        for e in self.client.call_sync('filesystem.list_dir', self.path):
            yield FileWrapRemote(
                PurePath(self.uri).joinpath(e['name']), type=e['type'], user=self.user, password=self.password)

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, val):
        self._freenas_mappings = {
            'DIRECTORY': 'dir',
            'FILE': 'file',
        }
        self.__type = self._freenas_mappings[val] if val else None

    def _get_type(self):
        #self.client.connect('ws://'+self.hostname)
        #self.client.login_user(self.user, self.password)
        """ TODO """
        return 'DIRECTORY'

    def _get_parent(self):
        return FileWrapRemote(PurePath(self.uri).parent.as_posix(), user=self.user, password=self.password)
