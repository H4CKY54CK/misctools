import os
import sys
import csv
import praw
import argparse
from math import sqrt, ceil, floor
from PIL import Image

def build_spritesheets(args=None):
    """Generate spritesheets."""

    for folder in os.scandir(args.source):
        if os.path.isdir(folder.path):
            images = []
            x, y = 0, 0
            for item in os.scandir(folder.path):
                exts = ['.png', '.jpg', '.jpeg']
                if item.name.endswith(tuple(exts)):
                    images.append(Image.open(item.path))
                    extension = os.path.splitext(item.path)[1]
            if len(images) > ceil(sqrt(len(images))) * floor(sqrt(len(images))):
                rows = ceil(sqrt(len(images))), ceil(sqrt(len(images)))
            else:
                rows = ceil(sqrt(len(images))), floor(sqrt(len(images)))
            canvas = (images[0].size[0] * rows[0], images[0].size[1] * rows[1])
            sprite = Image.new('RGBA', (canvas[0], canvas[1]))
            for img in images:
                sprite.paste(img, (x, y))
                x += img.size[0]
                if x >= canvas[0]:
                    x -= canvas[0]
                    y += img.size[1]
            spritesheet = os.path.join(args.output, f"flairs-{folder.name}{extension}")
            if args.size:
                height, width = args.size
                sprite.thumbnail((height * rows[0], width * rows[1]), Image.LANCZOS)
            else:
                height, width = images[0].size
            sprite.save(spritesheet, extension.lstrip('.'))
            print(f"Spritesheet `{os.path.basename(spritesheet)}` generated... You can find it in `{os.path.basename(args.output)}`.")

def build_stylesheet(args=None):
    """Generate stylesheet contents."""

    m = '\n'
    if args.minify:
        m = ''
    stylesheet = os.path.join(args.output, 'stylesheet.css')
    with open(stylesheet, 'w') as cssf:
        if args.size:
            height, width = args.size
        if args.site:
            reddit = praw.Reddit(args.site)
            subreddit = reddit.subreddit(reddit.config.custom['subreddit'])
            key = reddit.config.custom['key']
            sub_style = subreddit.stylesheet().stylesheet
            style = f"{sub_style.split(key)[0]}{key}{m}-------------*/{m}"
            cssf.write(style)
        for folder in os.scandir(args.source):
            path = os.path.join(args.source, folder.path)
            if os.path.isdir(path):
                line = f'{m}.flair[class*="{folder.name}-"] {{background-image: url(%%flairs-{folder.name}%%);}}{m}{m}'
                cssf.write(line)
                x, y = 0, 0
                images = 0
                for item in os.listdir(path):
                    images += 1
                if images > ceil(sqrt(images)) * floor(sqrt(images)):
                    rows = ceil(sqrt(images)), ceil(sqrt(images))
                else:
                    rows = ceil(sqrt(images)), floor(sqrt(images))
                for count, item in enumerate(os.scandir(path)):
                    if count == 0 and not args.size:
                        img = Image.open(item.path)
                        height, width = img.size
                    if item.name.endswith('_4.png'):
                        item = item.name.split('_4.png')[0]
                    elif item.name.endswith('.png'):
                        item = item.name.split('.png')[0]
                    part = f".flair-{folder.name}-{item} {{min-width: {width}px; background-position: {x}{'px' if x != 0 else ''} {y}{'px' if y != 0 else ''};}}{m}"
                    cssf.write(part)
                    x -= height
                    if -x == height * rows[0]:
                        x += height * rows[0]
                        y -= width

    print(f"Stylesheet `{os.path.basename(stylesheet)}` generated. You can find it in `{os.path.basename(args.output)}`.")

def build_flairs(args=None):
    """Generate dictionary for `flairs.csv.`"""

    flair_list = os.path.join(args.output, 'flairs.csv')
    with open(flair_list, 'w', newline='') as csvf:
        csvf = csv.writer(csvf)
        for folder in os.scandir(args.source):
            path = os.path.join(args.source, folder)
            if os.path.isdir(path):
                for item in os.listdir(path):
                    line1 = item.split('.png')[0]
                    line2 = f"{folder.name}-{line1}"
                    if item.endswith('_4.png'):
                        line2 = f"{folder.name}-{item.split('_4.png')[0]}"
                    csvf.writerow([line1,line2])

    print(f"Flair list `{os.path.basename(flair_list)}` generated. You can find it in `{os.path.basename(args.output)}`.")

def update_reddit(args=None):

    stylesheet = os.path.join(args.output, 'stylesheet.css')
    if args.site and args.update:
        reddit = praw.Reddit(args.site)
        subreddit = reddit.subreddit(reddit.config.custom['subreddit'])

        for item in os.listdir(args.output):
            path = os.path.join(os.path.abspath(args.output), item)
            ext = ['.png', '.jpg', '.jpeg']
            if item.lower().endswith(tuple(ext)):
                subreddit.stylesheet.upload(item.split('.')[0], path)
                print(f"Image `{item}` uploaded successfully as {item.split('.')[0]}")
            if item.lower().endswith('.css'):
                with open(stylesheet) as cssf:
                    style = cssf.read()
                    subreddit.stylesheet.update(style)
                    print(f"Stylesheet `{os.path.basename(stylesheet)}` updated succesfully.")

def process(args=None):
    if args.img_output:
        build_spritesheets(args)
    if args.css_output:
        build_stylesheet(args)
    if args.bot_files:
        build_flairs(args)
    if args.site and args.update:
        update_reddit(args)


def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source',
                        dest='source', type=str, nargs=1,
                        default=os.environ.get("SPRITEIT_SOURCE", None),
                        help='source directory of images')
    parser.add_argument('-o', '--output',
                        dest='output', type=str, nargs=1,
                        default=os.environ.get("SPRITEIT_OUTPUT", None),
                        help='output directory of spritesheets/stylesheet')
    parser.add_argument('-xy', '--size',
                        dest='size', type=int, nargs=2,
                        default=os.environ.get("SPRITEIT_IMG_SIZE"),
                        help='desired dimensions of individual images (separated by a space), \
                        resized before adding to spritesheet, and does not leave behind copies of \
                        files (example: `spriteit mypics -xy 50 50` to resize images to 50x50px, \
                        and then adding to the spritesheet)')
    parser.add_argument('-b', '--bot-files',
                        dest='bot_files', action='store_true', help='if you use the user flair \
                        bot, this option will generate a key:value csv file. for more info, see \
                        the README')
    parser.add_argument('-nc', '--no-css',
                        dest='css_output', action='store_false', help='skip generating the CSS, \
                        only generate the images')
    parser.add_argument('-ni', '--no-img',
                        dest='img_output', action='store_false', help='skip generating the images, \
                        only generate the CSS')
    parser.add_argument('-m', '--minify',
                        dest='minify', action='store_true',
                        help='minify the stylesheet after generation')
    parser.add_argument('-u', '--update',
                        dest='update', action='store_true', help='automatically update subreddit \
                        user flairs. includes uploading spritesheets and updating stylesheet. \
                        (requires -S/--site to also be used, as a precaution)')
    parser.add_argument('-S', '--site',
                        dest='site', type=str,
                        default=os.environ.get("SPRITEIT_SITE", None),
                        help='provide a config site from a pre-existing `praw.ini` \
                        file. must be in current working directory or APPDATA')
    parser.set_defaults(func=process)

    options, args = parser.parse_known_args(argv)

    extra = 0
    if not options.source and args:
        options.source = args[0]
        extra += 1

    if not options.output and args[extra:]:
        options.output = args[extra]
        extra += 1

    if options.source and options.output and args[extra:]:
        parser.error((f"Unrecognized arguments {args[extra:]}"))

    if options.source is None:
        parser.error("You must provide a source directory.")

    if not os.path.isdir(options.source):
        parser.error("Source directory not found.")

    options.source = os.path.abspath(options.source)

    if options.output is None:
        options.output = 'sprites'

    if options.output:
        options.output = os.path.abspath(options.output)

    if not os.path.exists(options.output):
        os.mkdir(options.output)

    options.func(options)

if __name__ == '__main__':
    sys.exit(main())
