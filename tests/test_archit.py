from filecmp import dircmp
import shutil
import time
import os
import requests
from urllib.request import urlopen
from io import BytesIO
import sys

rg = requests.get
url = 'https://picsum.photos/v2/list?page=2&limit=100'

os.chdir(os.path.abspath(os.path.dirname(__file__)))

home = os.getcwd()
st = os.path.join(home, 'subtests')
sst = os.path.join(st, 'subsubtests')

if not os.path.exists(st):
    os.mkdir(st)
if not os.path.exists(sst):
    os.mkdir(sst)


bckp = os.path.join(home, 'subtests-backup')

pics = rg(url)
jinfo = pics.json()
size = 0
ssize = 0
files = os.listdir(st)
sfiles = os.listdir(sst)
if not os.path.exists(bckp):
    if len(files) < 5 or len(sfiles) < 5:
        for x, y in enumerate(jinfo):
            durl = f"{y['download_url']}.jpg"
            name = f"{str(time.time())[:13]}.png"
            n1 = os.path.join(st, name)
            n2 = os.path.join(sst, name)
            if len(os.listdir(st)) < 5:
                with open(n1, 'wb') as f:
                    f.write(urlopen(durl).read())
            if len(os.listdir(sst)) <5:
                with open(n2, 'wb') as f:
                    f.write(urlopen(durl).read())
else:
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
    os.system('archit subtests -f zip tar gztar bztar xztar')
    os.rename(st, base)
    os.system('unarchit subtests.zip')
    current = dircmp(st, pbase)
    assert len(current.diff_files) == 0, f"problem with {st}"
    os.rename(st, pz)
    os.system('unarchit subtests.tar.gz')
    current = dircmp(st, pbase)
    assert len(current.diff_files) == 0, f"problem with {st}"
    os.rename(st, pgt)
    os.system('unarchit subtests.tar.bz2')
    current = dircmp(st, pbase)
    assert len(current.diff_files) == 0, f"problem with {st}"
    os.rename(st, pbt)
    os.system('unarchit subtests.tar.xz')
    current = dircmp(st, pbase)
    assert len(current.diff_files) == 0, f"problem with {st}"
    os.rename(st, pxt)
    os.system('unarchit subtests.tar')
    current = dircmp(st, pbase)
    assert len(current.diff_files) == 0, f"problem with {st}"
    os.rename(st, pt)
finally:
    for i in [base,pz,pbt,pgt,pxt,pt,zz,zxt,zgt,zbt,zt]:
        print(i)
        if os.path.exists(i):
            if os.path.isdir(i):
                shutil.rmtree(i)
            else:
                os.remove(i)