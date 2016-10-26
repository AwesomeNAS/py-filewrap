# coding=utf-8
#
# Copyright 2016 iXsystems, Inc.
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#####################################################################

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
