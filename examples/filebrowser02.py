import sys
import getpass
from filewrap import FileProvider


def cls():
    print('\n' * 100)

def print_examples():
    print("EXAMPLES:")
    print("FTP                            : 'ftp://localhost'")
    print("FTP (accepts anonymous user)   : 'ftp://ftp.funet.fi/pub/CPAN'")
    print("LOCAL                          : 'file:///Users/piotrgl/designs/ixsystems/work/work_filebrowser/v01/src'")
    print("REMOTE                         : 'remote://<freenas-host>/mnt/mypool/'")

open_cmd = ['open']
exit_cmd = ['exit']
credentials_cmds = ['set_remote_logpass', 'set_ftp_logpass', 'reset_remote_logpass', 'reset_ftp_logpass']
dir_cmds = ['cd', 'listdir', 'mkdir', 'rmdir']
file_cmds = []

remote_logpass = {'username': '', 'password': ''}
ftp_logpass = {'username': '', 'password': ''}

def run_cmd(cmd, args=[], obj=None):

    if cmd == 'set_remote_logpass':
        remote_logpass['username'] = input(">enter freenas user (optional, leave empty 'root') :")
        remote_logpass['password'] = getpass.getpass(">enter freenas password (optional):")
        return (str(obj) if obj else '', obj, open_cmd + credentials_cmds)

    if cmd == 'reset_remote_logpass':
        remote_logpass['username'] = ''
        remote_logpass['password'] = ''
        print("Remote FreeNAS login credentials reset")
        return (str(obj) if obj else '', obj, open_cmd + credentials_cmds)

    if cmd == 'set_ftp_logpass':
        ftp_logpass['username'] = input(">enter ftp user (optional, leave empty 'anonymous') :")
        ftp_logpass['password'] = getpass.getpass(">enter ftp password (optional):")
        return (str(obj) if obj else '', obj, open_cmd + credentials_cmds)

    if cmd == 'reset_ftp_logpass':
        ftp_logpass['username'] = ''
        ftp_logpass['password'] = ''
        print("Ftp login credentials reset")
        return (str(obj) if obj else '', obj, open_cmd + credentials_cmds)

    if cmd == 'open':
        dir = FileProvider.open(args[0], remote_logpass=remote_logpass, ftp_logpass=ftp_logpass)
        return (str(dir), dir, dir_cmds)

    if cmd == 'listdir':
        objs = [(o.name, o.type.name) for o in obj.readdir()]
        for i, e in enumerate(objs):
            print("{0}. Name: {1} | Type: {2}".format(i, e[0], e[1]))
        return (str(obj), obj, dir_cmds + exit_cmd)

    if cmd == 'cd':
        if args[0] == '..':
            dest = obj.parent
        elif args[0] == '.':
            dest = obj
        else:
            dest = obj.get_child(args[0])
        if dest.is_dir:
            return (str(dest), dest, dir_cmds + exit_cmd)
        else:
            raise ValueError('Cannot "cd" into object of type: {0}'.format(dest.type.name))

    if cmd == 'rmdir':
        obj.rmdir(args[0])
        return (str(obj), obj, dir_cmds + exit_cmd)

    if cmd == 'mkdir':
        obj.mkdir(args[0])
        return (str(obj), obj, dir_cmds + exit_cmd)

    if cmd == 'exit':
        print_examples()
        return ('', None, ['open'] + credentials_cmds)


def main():
    curr_obj = None
    curr_path = ''
    curr_cmds = ['open'] + credentials_cmds
    print_examples()
    while True:
        print("COMMANDS: ", curr_cmds)
        i = input(curr_path+">")
        cmd, *args = i.split(' ')
        curr_path, curr_obj, curr_cmds = run_cmd(cmd, args, curr_obj)


if __name__ == '__main__':
    sys.exit(main())
