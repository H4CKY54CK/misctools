import os
import sys
import argparse
import progressbar as pb
import urllib.request as req

def wdownload(args=None):
    url = args.url
    name = url.split('.com')[1]
    rpath = req.url2pathname(name)
    path = os.path.basename(rpath)
    filename = os.path.join(os.getcwd(), path)
    try:
        x = 0
        while os.path.exists(filename):
            x += 1
            fname, ext = filename.split('.')
            fname = fname.split(' ')[0]
            filename = f"{fname} ({x}).{ext}"
        with open(filename, 'wb') as f:
            f.write(req.urlopen(url).read())
        return f"{url} -> {filename}"
    except Exception:
        print(sys.exc_info())
        return f"Could not parse URL"

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help="the url you wish to download")
    parser.set_defaults(func=wdownload)
    args = parser.parse_args(argv)
    print(args.func(args))

if __name__ == '__main__':
    sys.exit(main())