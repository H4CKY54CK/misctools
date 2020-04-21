import os
import sys
import time
import shutil
import argparse
import traceback
import subprocess
from . import __version__

# Extra stuff to see where it goes.

def archit(args, options=None):
    # blue = '\033[38;2;30;144;255m'
    # underline = '\033[4m'
    # un1 = '\033[24m'
    # un2 = '\033[38;2;123;104;238m'
    args.output = args.output or args.source
    base_out = os.path.basename(args.output)
    errors = False
    print(f"\n\033[38;2;30;144;255m    \033[4mMisctools v{__version__}\033[24m\033[38;2;123;104;238m\n")
    try:
        for item in args.format:
            try:
                ext = f"tar.{item.split('tar')[0]}" if item != 'tar' and 'tar' in item else item
                print(f"    Creating archive {base_out}.{ext}...")
                shutil.make_archive(args.output, item, args.source)
                print(f"    Archive `{base_out}.{ext}` created...\n")
            except Exception as e:
                with open('archiving_errors.log', 'a') as f:
                    f.write(traceback.format_exc()+'\n')
                errors = True
    finally:
        if args.install:
            ext = f"tar.{args.sys.split('tar')[0]}" if args.sys != 'tar' and 'tar' in args.sys else args.sys
            print(f"    \033[38;2;255;165;0mPreparing to install `{base_out}.{ext}` via pip...\033[0m\n")
            os.system(f"{sys.executable} -m pip install {' '.join(options)} {args.output}.{ext}")
            print(f"\n    \033[38;2;255;165;0mFinished installing `{base_out}.{ext}`...\033[0m\n")
            print(f"    \033[38;2;255;165;0mCleaning up...\033[0m\n")
            os.remove(f'{args.output}.{ext}')
        if errors:
            print("    \033[38;2;50;252;50mFinished with errors. See `archiving_errors.log` for a more detailed report.\033[0m")
        else:
            print("    \033[38;2;50;252;50mFinished.\033[0m")
def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='package name in current directory you wish to compress')
    parser.add_argument('output', type=str, nargs='?', help='optionally specify an output name for the compressed file')
    parser.add_argument('-f', '--format', dest='format', type=str, choices=('zip', 'tar', 'gztar', 'bztar', 'xztar'), nargs='+', help="archive compression format (any combination of: 'zip', 'tar' (uncompressed), 'gztar', 'bztar', or 'xztar')")
    # parser.add_argument('-z', '--zip', dest='zip', action='store_true', help='choose this archive format')
    # parser.add_argument('-t', '--tar', dest='tar', action='store_true', help='choose this archive format')
    # parser.add_argument('-g', '--gztar', dest='gztar', action='store_true', help='choose this archive format')
    # parser.add_argument('-b', '--bztar', dest='bztar', action='store_true', help='choose this archive format')
    # parser.add_argument('-x', '--xztar', dest='xztar', action='store_true', help='choose this archive format')
    parser.add_argument('-i', '--install', dest='install', action='store_true', help='after creating the archive, install it via pip')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true')
    # parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='show all output')
    parser.set_defaults(func=archit)
    args, options = parser.parse_known_args(argv)
    args.sys = None
    if sys.platform == 'win32':
        args.sys = 'zip'
    else:
        args.sys = 'gztar'
    if not args.format:
        args.format = [args.sys]
    else:
        args.format.append(args.sys)
    args.func(args, options)
if __name__ == '__main__':
    sys.exit(main())
