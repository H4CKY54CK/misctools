import os
import shutil
import sys
import argparse
import begin
from glob import glob
from urllib.request import urlopen

sprint = sys.stdout.write

@begin.start
def wcit(*filenames):
    
    files = [f for g in filenames for f in glob(g)]
    chars = 0
    words = 0
    lines = 0
    system_dependent_shorthand = '\n' if os.name == 'nt' else ''
    output = []
    for file in files:
        try:
            with open(file, errors='ignore') as f:
                d = f.read()
            l = len(d.split('\n'))-1
            w = len(d.split())
            c = os.path.getsize(file)
            chars += c
            words += w
            lines += l
            output.append((l, w, c, file))
        except:
            pass
    if len(output) > 2:
        output.append((lines, words, chars, 'total'))
    w = max([len(str(i)) for i in (chars,words,lines)])
    ww = max([len(str(i)) for i in (files)])
    if w < 5:
        w = 5
    for item in output:
        sprint('{:>{width}} {:>{width}} {:>{width}} {:>{wwidth}}\n'.format(*item,width=w,wwidth=ww))


@begin.start
def wgetit(url, name=None):
    if name is None:
        name = os.path.split(url)[1]
    try:
        with open(name, 'wb') as f:
            f.write(urlopen(url).read())
            return f"{url} -> {name}"
    except Exception as e:
        return str(e)

def walk(path):
    d = [path]
    files = []
    while d:
        for item in os.scandir(d[0]):
            if item.is_dir():
                d.append(item.path)
            else:
                files.append(item.path)
        d.pop(0)
    return files

def search(args):

    if args.root:
        source = '/'
    elif args.source:
        found = False
        for root, dirnames, filenames in os.walk(os.path.expanduser('~')):
            for dirname in dirnames:
                if args.source.lower() == dirname.lower():
                    source = os.path.join(root, dirname)
                    found = True
                    break
            if found:
                break
    else:
        source = os.path.expanduser('~')

    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            if any(i.lower() in filename.lower() for i in args.files):
                print(os.path.abspath(os.path.join(root, filename)))

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('files', type=str, nargs='+')
    parser.add_argument('-s', '--source', dest='source', type=str, nargs='?')
    parser.add_argument('--root', action='store_true')
    parser.set_defaults(func=search)
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())