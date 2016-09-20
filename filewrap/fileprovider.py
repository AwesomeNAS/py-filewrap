from . import FileWrapLocal, FileWrapFtp, FileWrapRemote


class FileProvider(object):
    _local_prefix = "file://"
    _remote_prefix = "remote://"
    _ftp_prefix = "ftp://"

    @staticmethod
    def open(path, user=None, password=None):
        def strip_path(p):
            return p.split('://')[1]

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

    @staticmethod
    def _is_path_local(path):
        return path.startswith(FileProvider._local_prefix)

    @staticmethod
    def _is_path_remote(path):
        return path.startswith(FileProvider._remote_prefix)

    @staticmethod
    def _is_path_ftp(path):
        return path.startswith(FileProvider._ftp_prefix)
