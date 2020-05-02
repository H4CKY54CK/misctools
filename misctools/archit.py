import os
import sys
import time
import shutil
import argparse
import traceback
import subprocess
from . import __version__

def unarchit(args=None):

    source = os.path.abspath(args.source)
    base, suffix = os.path.splitext(source)
    if suffix.lower() in ['.gz', '.bz2', '.xz']:
        base, second = os.path.splitext(base)
        suffix = second + '.' + suffix.strip('.2')

    output = str(source).split(suffix)[0] if not args.output else args.output

    shutil.unpack_archive(source, output)
    if not args.quiet:
        print('Finished extracting.')
    if args.delete:
        os.remove(source)

def umain(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='zip file to extract')
    parser.add_argument('output', default=None, nargs='?', help='output destination directory')
    parser.add_argument('-D', '--delete', dest='delete', action='store_true', help="delete zip file after extraction")
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.set_defaults(func=unarchit)
    args = parser.parse_args(argv)
    args.func(args)


def archit(args, options=None):
    args.output = args.output or args.source
    base_out = os.path.basename(args.output)
    errors = False
    if not args.quiet:
        print(f"\n\033[38;2;30;144;255m    \033[4mMisctools v{__version__}\033[24m\033[38;2;123;104;238m\n")
    try:
        for item in args.format:
            try:
                ext = f"tar.{item.split('tar')[0]}" if item != 'tar' and 'tar' in item else item
                ext = 'tar.bz2' if item == 'bztar' else ext

                if not args.quiet:
                    print(f"    Creating archive {base_out}.{ext}...")
                shutil.make_archive(args.output, item, args.source)
                if not args.quiet:
                    print(f"    Archive `{base_out}.{ext}` created...\n")
            except Exception as e:
                with open('archiving_errors.log', 'a') as f:
                    f.write(traceback.format_exc()+'\n')
                errors = True
    finally:
        if args.install:
            ext = f"tar.{args.sys.split('tar')[0]}" if args.sys != 'tar' and 'tar' in args.sys else args.sys
            if not args.quiet:
                print(f"    \033[38;2;255;165;0mPreparing to install `{base_out}.{ext}` via pip...\033[0m\n")
            pkg = f"{args.output}.{ext}"
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, *options])
            # os.system(f"{sys.executable} -m pip install {' '.join(options)} {args.output}.{ext}")
            if not args.quiet:
                print(f"\n    \033[38;2;255;165;0mFinished installing `{base_out}.{ext}`...\033[0m\n")
            if not args.quiet:
                print(f"    \033[38;2;255;165;0mCleaning up...\033[0m\n")
            outpath = os.path.abspath(f'{args.output}.{ext}')
            os.remove(outpath)
        if errors:
            if not args.quiet:
                print("    \033[38;2;50;252;50mFinished with errors. See `archiving_errors.log` for a more detailed report.\033[0m")
        else:
            if not args.quiet:
                print("    \033[38;2;50;252;50mFinished.\033[0m")
def main(argv=None):

    argv = (argv or sys.argv)[1:]
    dformats = {"zip": "zip", "next": "xztar", "tar": "tar", "bz": "bztar", "bztar": "bztar", "bz2": "bztar", "gz": "gztar", "gztar": "gztar", "xz": "xztar", "xztar": "xztar", "all": ["bztar", "gztar", "zip", "tar", "xztar"]}
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='package name in current directory you wish to compress')
    parser.add_argument('output', type=str, nargs='?', help='optionally specify an output name for the compressed file')
    parser.add_argument('-f', '--format', dest='format', type=str, choices=dformats, nargs='+', help="archive compression format(s) desired")
    # parser.add_argument('-z', '--zip', dest='zip', action='store_true', help='choose this archive format')
    # parser.add_argument('-t', '--tar', dest='tar', action='store_true', help='choose this archive format')
    # parser.add_argument('-g', '--gztar', dest='gztar', action='store_true', help='choose this archive format')
    # parser.add_argument('-b', '--bztar', dest='bztar', action='store_true', help='choose this archive format')
    # parser.add_argument('-x', '--xztar', dest='xztar', action='store_true', help='choose this archive format')
    parser.add_argument('-i', '--install', dest='install', action='store_true', help='after creating the archive, install it via pip')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='keep quiet')
    parser.set_defaults(func=archit)
    args, options = parser.parse_known_args(argv)
    args.sys = None
    if sys.platform == 'win32':
        args.sys = 'zip'
    else:
        args.sys = 'gztar'
    if not args.format:
        args.format = [args.sys]
    elif 'all' in args.format:
        args.format = dformats['all']
    else:
        args.format = [dformats[item] for item in args.format]
        args.format.append(args.sys)
    args.func(args, options)
