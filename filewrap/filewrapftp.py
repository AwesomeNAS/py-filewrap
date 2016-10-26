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
