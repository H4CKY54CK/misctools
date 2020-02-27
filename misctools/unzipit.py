import os
import sys
import zipfile
import argparse
import progressbar


def unzipit(args=None):


    start = "\033[38;5;46m"
    end = "\033[39m\033[49m"
    bar = progressbar.progressbar
    widgets = ['[ ', progressbar.Percentage(), ' ]', start, progressbar.Bar(), end, '[ ', progressbar.AdaptiveETA(), ' ]',]
    with zipfile.ZipFile(args.source) as z:
        for item in bar(z.namelist(), widgets=widgets):
            dirname = os.path.splitext(args.source)[0]
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            path = os.path.join(os.getcwd(), dirname)
            z.extract(item, path=path)
    print("Enjoy!")
    sys.exit()

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='zip file to extract')
    parser.add_argument('-D', '--delete', dest='delete', action='store_true', help="delete zip file after extraction")
    parser.set_defaults(func=unzipit)
    args = parser.parse_args(argv)
    args.func(args)
    

if __name__ == '__main__':
    sys.exit(main())
