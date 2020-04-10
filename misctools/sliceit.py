import sys
import os
import argparse
import math
from PIL import Image

def sliceit(args):

    with Image.open(source) as img:
        height = img.height
        width = img.width
    rows = math.ceil(height / h)
    cols = math.ceil(width / w)
    total = rows * cols
    print(total)

    zf = len(str(total))
    x = 0
    y = 0
    xx = w
    yy = h
    z = 0
    img = Image.open(source)
    while True:
        base, ext = os.path.splitext(source)
        output = f"{base}-{str(z).zfill(zf)}{ext}"
        if xx > width:
            x = 0
            xx = w
            y += h
            yy += h
        if yy > height:
            print("All done!")
            sys.exit()
        box = (x,y,xx,yy)
        img.crop(box).save(output)
        x += w
        xx += w
        z += 1

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('height', type=str)
    parser.add_argument('width', type=str)
    parser.set_defaults(func=sliceit)
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
