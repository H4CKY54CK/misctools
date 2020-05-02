import os
import sys
# import argparse
# import subprocess
import re
# from glob import glob
import begin
from glob import glob

# def run_ipy(args):

#     v = args.version.replace('.', '')
#     v = v.replace('-', '')
#     path = os.path.abspath(os.path.dirname(os.path.dirname(sys.executable)))

#     command = os.path.join(path, f'Python{v}', 'Scripts', 'ipython.exe')
#     try:
#         subprocess.run(command)
#     except Exception as e:
#         print("You don't have that version of iPython.")

# def main(argv=None):
#     argv = (argv or sys.argv)[1:]
#     parser = argparse.ArgumentParser()
#     parser.add_argument('version', type=str)
#     parser.set_defaults(func=run_ipy)
#     args = parser.parse_args(argv)
#     args.func(args)


# @begin.start
# def ecython(*files):
#     files = [f for g in files for f in glob(g)]
    


@begin.start
def wcit(*filenames):
    # files = [f for g in filenames for f in glob(g)]
    files = [f for g in filenames for f in glob(g)]
    chars = 0
    words = 0
    lines = 0
    sys.stdout.write(f"\n{'lines':<10}{'words':<10}{'chars':<10}\n")
    for file in files:
        with open(file) as f:
            d = f.read()
        l = len(d.split('\n'))-1
        w = len(d.split())
        c = os.path.getsize(file)
        # w = len(re.findall(r'\S+', data))
        # l = len(re.findall(r'\n', data))
        chars += c
        words += w
        lines += l
        sys.stdout.write(f"{l:<10}{w:<10}{c:<10}{file:<30}\n")
    if c != chars:
        sys.stdout.write(f"{lines:<10}{words:<10}{chars:<10}{'total':<10}\n")


# def wcit(args):
#     argv = (argv or sys.argv)[1:]
#     parser = argparse.ArgumentParser()
#     parser.add_argument('files', type=str, nargs='*')
#     parser.set_defaults(func=wcit)
#     args = parser.parse_args(argv)
#     args.func(args)


# if __name__ == '__main__':
#     sys.exit(main())