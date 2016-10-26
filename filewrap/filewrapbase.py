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

from enum import Enum
from pathlib import PurePath


class FileWrapBase(object):
    def __init__(self, uri, type=None):
        def split_uri(uri):
            return (PurePath(uri).parts[0], PurePath('/', *PurePath(uri).parts[1:]).as_posix())

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
        for d in self.readdir():
            if d.name == name:
                return d
        raise ValueError('Error: Directory/file does not exist: {0}'.format(name))

    def _map_type(self, val):
        raise NotImplementedError

    def _get_type(self):
        raise NotImplementedError

    def _get_parent(self):
        raise NotImplementedError


class FileType(Enum):
    dir = 1
    file = 2
    symlink = 3
