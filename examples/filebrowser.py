import sys
import getpass
from filewrap import FileProvider


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def main():
    def print_files(files):
        for i, f in enumerate(files):
            print("f.uri={0}, INDEX:{1}".format(f.uri, i))

    while True:
        i = input(">enter ftp/freenas user (optional, leave empty for 'anonymous'/'root') :")
        _user = i
        i = getpass.getpass(">enter ftp/freenas password (optional):")
        _password = i
        print("EXAMPLES:")
        print("FTP                            : 'ftp://localhost'")
        print("FTP (accepts anonymous user)   : 'ftp://ftp.funet.fi/pub/CPAN'")
        print("LOCAL                          : 'file:///Users/piotrgl/designs/ixsystems/work/work_filebrowser/v01/src'")
        print("REMOTE                         : 'remote://<freenas-host>/mnt/mypool/'")
        i = input(">enter path:")
        currdir = FileProvider.open(i, user=_user, password=_password)
        files = [f for f in currdir.readdir()]
        print_files(files)
        while True:
            i = input(">Select index ('k'=restart, 'm'=mkdir, 'r'=rmdir, 'enter'=navigate up):")
            if i == 'k':
                break
            elif i == 'm':
                i = input(">Dirname:")
                currdir.mkdir(i)
            elif i == 'r':
                currdir.rmdir()
                currdir = currdir.parent
            elif is_number(i) :
                if int(i) < len(files) and files[int(i)].is_dir:
                    currdir = files[int(i)]
                else:
                    continue
            else:
                currdir = currdir.parent
            files = [f for f in currdir.readdir()]
            print_files(files)


if __name__ == '__main__':
    sys.exit(main())
