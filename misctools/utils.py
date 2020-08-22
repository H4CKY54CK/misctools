import os
import shutil
import sys
import argparse

def search(args):

    if args.root:
        source = '/'
    elif args.source:
        found = False
        for root, dirnames, filenames in os.walk(os.path.expanduser('~')):
            for dirname in dirnames:
                if args.source.lower() == dirname.lower():
                    source = os.path.join(root, dirname)
                    found = True
                    break
            if found:
                break
    else:
        source = os.path.expanduser('~')

    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            if any(i.lower() in filename.lower() for i in args.files):
                print(os.path.abspath(os.path.join(root, filename)))


def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('files', type=str, nargs='+')
    parser.add_argument('-s', '--source', dest='source', type=str, nargs='?')
    parser.add_argument('--root', action='store_true')
    parser.set_defaults(func=search)
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())