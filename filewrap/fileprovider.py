from urllib.parse import urlparse
from . import FileWrapLocal, FileWrapFtp, FileWrapRemote


class FileProvider(object):
    _scheme_local = "file"
    _scheme_remote = "remote"
    _scheme_ftp = "ftp"

    @staticmethod
    def open(path, user=None, password=None):
        def strip_path(p):
            o = urlparse(p)
            return o.netloc + o.path


        kwargs = {}
        if user:
            kwargs['user'] = user
        if password:
            kwargs['password'] = password
        if FileProvider._is_path_local(path):
            return FileWrapLocal(strip_path(path))
        elif FileProvider._is_path_remote(path):
            return FileWrapRemote(strip_path(path), **kwargs)
        elif FileProvider._is_path_ftp(path):
            return FileWrapFtp(strip_path(path), **kwargs)
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
