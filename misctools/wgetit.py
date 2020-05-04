# import os
# import sys
# import argparse
# from urllib.request import urlopen
# def wdownload(args=None):
#     url = args.url
#     name = os.path.basename(url)
#     try:
#         with open(name, 'wb') as f:
#             f.write(urlopen(url).read())
#             return f"{url} -> {name}"
#     except Exception as e:
#         return str(e)
# def main(argv=None):
#     argv = (argv or sys.argv)[1:]
#     parser = argparse.ArgumentParser()
#     parser.add_argument('url', type=str, help="the url you wish to download")
#     parser.set_defaults(func=wdownload)
#     args = parser.parse_args(argv)
#     print(args.func(args))
# if __name__ == '__main__':
#     sys.exit(main())