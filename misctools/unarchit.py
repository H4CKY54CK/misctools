from pathlib import Path
import os
import sys
import argparse
import shutil

def unzipit(args=None):

    source = os.path.abspath(args.source)
    source = Path(args.source).absolute()
    output = str(source).split(''.join(source.suffixes))[0] if not args.output else args.output
    shutil.unpack_archive(source, output)
    print('Finished extracting.')
    if args.delete:
        os.remove(source)


    # for item in os.scandir(os.getcwd()):
    #     name, ext = os.path.splitext(item.name)
    #     if args.source.lower() == name.lower() or args.source.lower() == item.name.lower():
    #         shutil.unpack_archive(item.path, os.path.splitext(item.path)[0])
    #         print("Finished extracting.")
    #         if args.delete:
    #             os.remove(item)

# def main(argv=None):
#     argv = (argv or sys.argv)[1:]
#     parser = argparse.ArgumentParser()
#     parser.add_argument('source', help='zip file to extract')
#     parser.add_argument('output', default=None, nargs='?', help='output destination directory')
#     parser.add_argument('-D', '--delete', dest='delete', action='store_true', help="delete zip file after extraction")
#     parser.set_defaults(func=unzipit)
#     args = parser.parse_args(argv)
#     args.func(args)
    

# if __name__ == '__main__':
#     sys.exit(main())
