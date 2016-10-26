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

from urllib.parse import urlparse
from . import FileWrapLocal, FileWrapFtp, FileWrapRemote


class FileProvider(object):
    _scheme_local = "file"
    _scheme_remote = "remote"
    _scheme_ftp = "ftp"

    @staticmethod
    def open(path, remote_logpass={}, ftp_logpass={}):
        """
        :param path: str
        :param remote_logpass: {'username': '<username>', 'password': '<password>'}
        :param ftp_logpass: {'username': '<username>', 'password': '<password>'}
        :return: FileWrapBase compatible object
        """
        def strip_path(p):
            o = urlparse(p)
            return o.netloc + o.path

        if FileProvider._is_path_local(path):
            return FileWrapLocal(strip_path(path))
        elif FileProvider._is_path_remote(path):
            return FileWrapRemote(strip_path(path), **remote_logpass)
        elif FileProvider._is_path_ftp(path):
            return FileWrapFtp(strip_path(path), **ftp_logpass)
        else:
            raise ValueError('Unrecognized uri scheme type')

    @staticmethod
    def _is_path_local(path):
        return urlparse(path).scheme == FileProvider._scheme_local

    @staticmethod
    def _is_path_remote(path):
        return urlparse(path).scheme == FileProvider._scheme_remote

    @staticmethod
    def _is_path_ftp(path):
        return urlparse(path).scheme == FileProvider._scheme_ftp
