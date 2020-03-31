import os
import sys
from PIL import Image
from argparse import ArgumentParser as AP


def gifit(args=None, directory=None):

    if directory is None:
        source = args.source
    if not args.output.endswith('.gif'):
        output = f"{args.output.rstrip('.gif')}.gif"
    else:
        output = args.output

    images = [Image.open(os.path.join(os.path.abspath(source), item)) for item in os.listdir(source)]
    images[0].save(output, save_all=True, append_images=images[1:], loop=0)
    print(f"Gif {output} created. Enjoy!")
    if sys.platform == 'win32':
        os.system(output)

def main(argv=None):

    argv = (argv or sys.argv)[1:]
    parser = AP()
    parser.add_argument('source', type=str, help='source directory to make the gif with')
    parser.add_argument('output', type=str, help='the desired final output filename')
    parser.set_defaults(func=gifit)
    args = parser.parse_args(argv)
    try:
        args.func(args=args)
    except Exception as e:
        parser.error((str(e)))

if __name__ == '__main__':
    sys.exit(main())