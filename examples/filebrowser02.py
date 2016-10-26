import sys
from filewrap import FileProvider


def cls():
    print('\n' * 100)


def run_cmd(cmd, args=[], obj=None):
    if cmd == 'open':
        dir = obj.open(args[0])
        return (str(dir), dir, ['cd', 'listdir'])

    if cmd == 'listdir':
        objs = [(o.name, o.type.name) for o in obj.readdir()]
        for i, e in enumerate(objs):
            print("{0}. Name: {1} | Type: {2}".format(i, e[0], e[1]))
        return (str(obj), obj, ['cd', 'listdir'])

    if cmd == 'cd':
        if args[0] == '..':
            dest = obj.parent
        elif args[0] == '.':
            dest = obj
        else:
            dest = obj.get_child(args[0])
        if dest.is_dir:
            return (str(dest), dest, ['cd', 'listdir'])
        else:
            raise ValueError('Cannot "cd" into object of type: {0}'.format(dest.type.name))


def main():
    curr_obj = FileProvider()
    curr_path = ''
    curr_cmds = ['open']
    while True:
        print("Commands: ", curr_cmds)
        i = input(curr_path+">")
        cmd, *args = i.split(' ')
        curr_path, curr_obj, curr_cmds = run_cmd(cmd, args, curr_obj)


if __name__ == '__main__':
    sys.exit(main())
