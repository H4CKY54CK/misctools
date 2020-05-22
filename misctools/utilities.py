import os
import sys
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
        with open(file) as f:
            d = f.read()
        l = len(d.split('\n'))-1
        w = len(d.split())
        c = os.path.getsize(file)
        chars += c
        words += w
        lines += l
        output.append((l, w, c, file))
    if len(output) > 2:
        output.append((lines, words, chars, 'total'))
    w = max([len(str(i)) for i in (chars,words,lines)])
    if w < 5:
        w = 5
    for item in output:
        sprint('{:>{width}} {:>{width}} {:>{width}} {:>{width}}\n'.format(*item,width=w))


@begin.start
def wgetit(url, name):
    try:
        with open(name, 'wb') as f:
            f.write(urlopen(url).read())
            return f"{url} -> {name}"
    except Exception as e:
        return str(e)
