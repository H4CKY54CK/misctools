import os
import sys
import begin
from glob import glob

@begin.start
def wcit(*filenames):
    files = [f for g in filenames for f in glob(g)]
    chars = 0
    words = 0
    lines = 0
    sys.stdout.write(f"\n{'lines':<10}{'words':<10}{'chars':<10}\n")
    for file in files:
        with open(file) as f:
            d = f.read()
        l = len(d.split('\n'))-1
        w = len(d.split())
        c = os.path.getsize(file)
        chars += c
        words += w
        lines += l
        sys.stdout.write(f"{l:<10}{w:<10}{c:<10}{file:<30}\n")
    if c != chars:
        sys.stdout.write(f"{lines:<10}{words:<10}{chars:<10}{'total':<10}\n")

@begin.start
def wgetit(url, name):
    try:
        with open(name, 'wb') as f:
            f.write(urlopen(url).read())
            return f"{url} -> {name}"
    except Exception as e:
        return str(e)
