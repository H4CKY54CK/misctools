import sys
import os
import argparse
import math
from PIL import Image

def sliceit(args):

    with Image.open(args.source) as img:
        height = img.height
        width = img.width
    rows = math.ceil(height / args.height)
    cols = math.ceil(width / args.width)
    total = rows * cols
    print(total)

    zf = len(str(total))
    x = 0
    y = 0
    xx = args.width
    yy = args.height
    z = 0
    img = Image.open(args.source)
    while True:
        base, ext = os.path.splitext(args.source)
        output = f"{base}-{str(z).zfill(zf)}{ext}"
        if xx > width:
            x = 0
            xx = args.width
            y += args.height
            yy += args.height
        if yy > height:
            print("All done!")
            sys.exit()
        box = (x,y,xx,yy)
        img.crop(box).save(output)
        x += args.width
        xx += args.width
        z += 1

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('height', type=int)
    parser.add_argument('width', type=int)
    parser.set_defaults(func=sliceit)
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
