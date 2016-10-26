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
