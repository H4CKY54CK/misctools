import sys
import traceback
import shutil
import argparse
import subprocess
def archit(args):
    args.output = args.output or args.source
    ret = '\r'
    if args.verbose:
        ret = '\n'
    errors = False
    print(f"\n\033[38;2;30;144;255m    \033[4mMisctools v1.5dev\033[24m\033[38;2;123;104;238m\n")
    try:
        for item in args.format:
            try:
                print(f"    Creating archive {args.output}.{item}...", end=ret)
                shutil.make_archive(args.output, item, args.source)
                print(f"    Archive `{args.output}.{item}` created...")
            except Exception as e:
                with open('archiving_errors.log', 'a') as f:
                    f.write(traceback.format_exc())
                errors = True
    finally:
        if args.install:
            print(f"    \033[38;2;255;165;0mPreparing to install `{args.output}.{args.sys}` via pip...\033[0m")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', f"{args.output}.{args.sys}"])
            print(f"    \033[38;2;255;165;0mFinished installing `{args.output}.{args.sys}`...\033[0m\n")
        if errors:
            print("\n\n\033[38;2;50;252;50m    Finished with errors. See `archiving_errors.log` for a more detailed report.\033[0m\n")
        else:
            print("\n\n\033[38;2;50;252;50m    Finished.\033[0m\n")
def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='package name in current directory you wish to compress')
    parser.add_argument('output', type=str, nargs='?', help='optionally specify an output name for the compressed file')
    parser.add_argument('-f', '--format', dest='format', type=str, nargs='+', help="archive compression format (one or more of: 'zip', 'tar' (uncompressed), 'gztar', 'bztar', or 'xztar')")
    parser.add_argument('-i', '--install', dest='install', action='store_true', help='after creating the archive, install it via pip')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='show all output')
    parser.set_defaults(func=archit)
    args = parser.parse_args(argv)
    args.sys = None
    if sys.platform == 'win32':
        args.sys = 'zip'
    else:
        args.sys = 'gztar'
    if not args.format:
        args.format = [args.sys]
    else:
        args.format.append(args.sys)
    args.func(args)
if __name__ == '__main__':
    sys.exit(main())
