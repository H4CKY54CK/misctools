import os
import sys
import tarfile
import zipfile
import argparse
import platform
import subprocess
from tqdm import tqdm

def zipit(args=None):

    if args.zip or platform.system().casefold() == 'windows' and not args.tar and not args.zip:
        if not args.output:
            output_zip = args.source + '.zip'
        try:
            print("Putting together your zip file... Please hold.")
            items = []
            zip_file = zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED)
            for dirpath, dirnames, filenames in os.walk(args.source):
                for filename in filenames:
                    items.append(os.path.join(dirpath, filename))
            for item in tqdm(items, desc='Progress'):
                zip_file.write(item)
            print(f"Archive `{output_zip}` successfully created.")
            no_errors = True
        except IOError as e:
            print(e)
            sys.exit(1)
        except OSError as e:
            print(e)
            sys.exit(1)
        except zipfile.BadZipfile as e:
            print(e)
            sys.exit(1)
        finally:
            zip_file.close()

        if args.install and no_errors:
            subprocess.run([sys.executable, '-m', 'pip', 'install', output_zip])
            print("Cleaning up...")
            os.remove(output_zip)

    if not args.zip and platform.system().casefold() == 'linux' or args.tar:
        if not args.output:
            output_tar = args.source + '.tar.gz'
        tars = []
        print("Putting together your tar.gz file... Please hold.")
        try:
            for root, dirs, files in os.walk(args.source):
                for file in files:
                    tars.append(os.path.join(root, file))
            with tarfile.open(output_tar, 'w:gz') as tar_handle:
                for item in tqdm(tars, desc='Progress'):
                    tar_handle.add(item)
            print(f"Archive `{output_tar}` successfully created.")
            no_errors = True
        except IOError as e:
            print(e)
            sys.exit(1)
        except OSError as e:
            print(e)
            sys.exit(1)
        finally:
            tar_handle.close()

        if args.install and no_errors:
            subprocess.run([sys.executable, '-m', 'pip', 'install', output_tar])
            print("Cleaning up...")
            os.remove(output_tar)


def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='package name in current directory you wish to compress')
    parser.add_argument('output', type=str, nargs='?', help='optionally specify an output name for the compressed file')
    parser.add_argument('-z', '--zip', dest='zip', action='store_true', help='use `--zip/-z` if you want to force it to create a zip file on Linux (or if it is incorrectly guessing your OS)')
    parser.add_argument('-t', '--tar', dest='tar', action='store_true', help='use `--tar/-t` if you want to force it to create a tar file on Windows (or if it is incorrectly guessing your OS)')
    parser.add_argument('-i', '--install', dest='install', action='store_true', help='install this zip/tar file via pip, after creating zip/tar file')
    parser.set_defaults(func=zipit)
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
