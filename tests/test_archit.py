from filecmp import dircmp
import shutil
import time
import os
from io import BytesIO
import sys


class Error:
    def __init__(self, msg):
        print(f"\033[38;2;255;0;0m(ERROR)\033[0m Could not find: {msg}")

def main():
    home = os.getcwd()
    st = os.path.join(home, 'subtests')
    sst = os.path.join(st, 'subsubtests')
    if not os.path.exists(st):
        os.mkdir(st)
    if not os.path.exists(sst):
        os.mkdir(sst)
    bckp = os.path.join(home, 'subtests-backup')
    if os.path.exists(bckp) and not os.path.exists(st):
        shutil.copytree(bckp, st)
    base = 'subtests-base'
    pbase = os.path.join(home, 'subtests-base')
    z = 'subtests-zip'
    zz = 'subtests.zip'
    pz = os.path.join(home, 'subtests-zip')
    bt = 'subtests-bztar'
    zbt = 'subtests.tar.bz2'
    pbt = os.path.join(home, 'subtests-bztar')
    gt = 'subtests-gztar'
    zgt = 'subtests.tar.gz'
    pgt = os.path.join(home, 'subtests-gztar')
    xt = 'subtests-xztar'
    zxt = 'subtests.tar.xz'
    pxt = os.path.join(home, 'subtests-xztar')
    t = 'subtests-tar'
    zt = 'subtests.tar'
    pt = os.path.join(home, 'subtests-tar')
    try:
        os.system('archit subtests -f zip tar gztar bztar xztar -q')
        os.rename(st, base)
        os.system('unarchit subtests.zip -q')
        assert len(dircmp(st, pbase).diff_files) == 0, f"problem with {st}"
        os.rename(st, pz)
        os.system('unarchit subtests.tar.gz -q')
        assert len(dircmp(st, pbase).diff_files) == 0, f"problem with {st}"
        os.rename(st, pgt)
        os.system('unarchit subtests.tar.bz2 -q')
        assert len(dircmp(st, pbase).diff_files) == 0, f"problem with {st}"
        os.rename(st, pbt)
        os.system('unarchit subtests.tar.xz -q')
        assert len(dircmp(st, pbase).diff_files) == 0, f"problem with {st}"
        os.rename(st, pxt)
        os.system('unarchit subtests.tar -q')
        assert len(dircmp(st, pbase).diff_files) == 0, f"problem with {st}"
        os.rename(st, pt)
    except FileNotFoundError:
        Error(st)
    finally:
        for i in [base,pz,pbt,pgt,pxt,pt,zz,zxt,zgt,zbt,zt]:
            if os.path.exists(i):
                if os.path.isdir(i):
                    shutil.rmtree(i)
                else:
                    os.remove(i)
        print("\033[38;2;0;255;0mAll Tests Passed\033[0m")

if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    sys.exit(main())