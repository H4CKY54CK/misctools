from tqdm import tqdm
import zipfile
import os
import sys
import argparse
import subprocess


def zipit(args):
    try:
        output = f"{args.source}.zip"
        dirs = [args.source]
        files = []
        while dirs:
            for item in os.scandir(dirs[0]):
                if item.is_dir():
                    dirs.append(item.path)
                files.append(item.path)
            dirs.pop(0)
        zipped = zipfile.ZipFile(output, 'w')
        print("Zipping files...")
        for item in tqdm(files):
            zipped.write(item)
        zipped.close()
        if args.install:
            print("Installing...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', output])
    except Exception as e:
        print(e)
    finally:
        print('Cleaning up...', end='\r')
        os.remove(output)
        print('Done.         ')

def unzipit(args):
    print("Unzipping.")
    zipped = zipfile.ZipFile(args.source)
    for item in tqdm(zipped.namelist()):
        zipped.extract(item)
    print("Done.")



def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('--install', '-i', action='store_true')
    parser.set_defaults(func=zipit)
    args = parser.parse_args(argv)
    args.func(args)

def umain(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.set_defaults(func=unzipit)
    args = parser.parse_args(argv)
    args.func(args)



if __name__ == '__main__':
    sys.exit(main())