import os
import sys
import zipfile
import argparse
import tarfile
from tqdm import tqdm

def unzipit(args=None):

    if zipfile.is_zipfile(args.source):
        with zipfile.ZipFile(args.source) as z:
            memb = list(z.namelist())
            path = os.path.splitext(args.source)[0]
                os.mkdir(path)
            if not os.path.exists(path):
            for item in tqdm(memb, desc="Progress"):
                z.extract(item, path=args.output if args.output is not None else None)

    elif tarfile.is_tarfile(args.source):
        with tarfile.open(args.source) as t:
            memb = list(t.getmembers())
            path = args.source.split('.tar.gz')[0]
                os.mkdir(path)
            if not os.path.exists(path):
            for item in tqdm(memb, desc="Progress"):
                t.extract(item, path=args.output if args.output is not None else None)
    print("Enjoy!")
    sys.exit()

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='zip file to extract')
    parser.add_argument('output', default=None, nargs='?', help='output destination directory')
    parser.add_argument('-D', '--delete', dest='delete', action='store_true', help="delete zip file after extraction")
    parser.set_defaults(func=unzipit)
    args = parser.parse_args(argv)
    args.func(args)
    

if __name__ == '__main__':
    sys.exit(main())
