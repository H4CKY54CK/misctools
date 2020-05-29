import os
import sys
import csv
import praw
import argparse
from math import sqrt, ceil, floor
from PIL import Image



def start(args=None):
    if not args.project:
        single_sheet(args)
    else:
        multi_sheet(args)


def single_sheet(args):
    images = [file.path for file in os.scandir(args.source)]
    if args.output is None:
        args.output = args.source
    if len(images) > ceil(sqrt(len(images))) * floor(sqrt(len(images))):
        rows, cols = ceil(sqrt(len(images))), ceil(sqrt(len(images)))
    else:
        rows, cols = ceil(sqrt(len(images))), floor(sqrt(len(images)))
    size = Image.open(images[0]).size
    canvas = (size[0]*rows,size[1]*cols)
    x = y = 0
    sheet = Image.new('RGBA', canvas)
    for item in images:
        sheet.paste(Image.open(item), (x,y))
        x += size[0]
        if x >= canvas[0]:
            x = 0
            y += size[1]
    if args.width and args.height:
        sheet = sheet.resize((args.width*rows, args.height*cols), Image.LANCZOS)
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    sheet.save(os.path.join(args.output, '{}.png'.format(args.output)),'PNG')
    generate_stylesheet(args)

def generate_stylesheet(args):
    images = [file for file in os.scandir(args.source)]
    size = Image.open(images[0].path).size
    if args.width and args.height:
        size = (args.width,args.height)
    x = y = 0
    if len(images) > ceil(sqrt(len(images))) * floor(sqrt(len(images))):
        rows, cols = ceil(sqrt(len(images))), ceil(sqrt(len(images)))
    else:
        rows, cols = ceil(sqrt(len(images))), floor(sqrt(len(images)))
    stylesheet = os.path.join(args.output,'stylesheet.css')
    lines = []
    folder = ''
    if args.project:
        folder = os.path.dirname(images[0].path) + '-'
        line = f'\n.flair[class*="{folder[:-1]}-"] {{background-image: url(%%flairs-{folder[:-1]}%%);}}\n\n'
        lines.append(line)
    for item in images:
        line = f".flair-{folder}{item.name.replace('.png', '')} {{min-width: {size[0]}px; background-position: -{x}{'px' if x != 0 else ''} -{y}{'px' if y != 0 else ''};}}\n"
        x += size[0]
        if x >= size[0] * rows:
            x = 0
            y += size[1]
        lines.append(line)
    with open(stylesheet, 'w') as f:
        f.writelines(lines)


def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('output', nargs='?')
    parser.add_argument('-p', '--project', dest='project', action='store_true')
    parser.add_argument('-x', '--width', dest='width', type=int, const=None)
    parser.add_argument('-y', '--height', dest='height', type=int, const=None)
    # parser.add_argument('output')
    parser.set_defaults(func=start)
    args,options = parser.parse_known_args(argv)
    if args.output is None:
        args.output = 'sprites'
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())