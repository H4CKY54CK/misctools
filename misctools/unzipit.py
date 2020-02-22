import os
import sys
import zipfile
import argparse
import progressbar


def unzipit(args=None):

    items = []
    zip_path = os.path.abspath(args.source)
    if zipfile.is_zipfile(zip_path):
        items.append(zip_path)
    else:
        try:
            for item in os.scandir(zip_path):
                if zipfile.is_zipfile(item.path):
                    items.append(item.path)
        except Exception as e:
            print(e)
            sys.exit(1)

    start = "\033[38;5;46m"
    end = "\033[39m\033[49m"

    try:
        print("Unzipping...")
        
        bar = progressbar.ProgressBar(max_value=8760, widgets=[' [', progressbar.Percentage(), '] ', start, progressbar.Bar(), end, ' (', progressbar.AdaptiveETA(), ') ',]).start()

        for count, item in enumerate(items):
            with zipfile.ZipFile(item) as zip_file:
                name = os.path.basename(os.path.abspath(item)).split('.zip')[0]
                parent_folder = os.path.dirname(item)
                zip_file.extractall(os.path.join(parent_folder, name))
                if args.delete:
                    os.remove(item)
            bar.update(count+1)
        bar.finish()
    except Exception as e:
        print(e)
        sys.exit(1)

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
