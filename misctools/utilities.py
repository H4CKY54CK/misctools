import os
import sys
import platform
import argparse
import subprocess

def run_ipy(args):

    command = r"C:\Users\tk13x\AppData\Local\Programs\Python\Python38\Scripts\ipython" + f"{args.version}.exe"

    subprocess.run(command)


def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('version')
    parser.set_defaults(func=run_ipy)
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())