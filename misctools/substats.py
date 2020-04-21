import os
import sys
import praw
from datetime import datetime
from collections import defaultdict
import msvcrt
import argparse
from praw.exceptions import MissingRequiredAttributeException

def substatter(args):

    # if args.site is None:
        # try:
        #     username = os.getenv('praw_username', None)
        #     passwd = os.getenv('praw_passwd', None)
        #     user_agent = os.getenv('praw_user_agent', None)
        #     client_id = os.getenv('praw_client_id', None)
        #     client_secret = os.getenv('praw_client_secret', None)
    #     except:
    #         sys.stderr.write('you must provide some kind of login details to access reddit with')
    # site = args.site or os.environ.get

    try:
        reddit = praw.Reddit(args.site)
    except MissingRequiredAttributeException:
        try:
            username = os.getenv('praw_username', None)
            passwd = os.getenv('praw_passwd', None)
            user_agent = os.getenv('praw_user_agent', None)
            client_id = os.getenv('praw_client_id', None)
            client_secret = os.getenv('praw_client_secret', None)
            reddit = praw.Reddit(username=username, passwd=passwd, user_agent=user_agent, client_id=client_id, client_secret=client_secret)
        # except MissingRequiredAttributeException as e:
        #     print(f"{e}")
        #     sys.exit()
        except Exception as e:
            print(f"{e}")
            sys.exit()


    sub = args.subreddit or reddit.custom.config['subreddit']

    print(f"Working... Please be patient...", end='\r')

    subreddit = reddit.subreddit(sub)
    sname = subreddit.display_name

    ts = datetime.now()

    comments = list(subreddit.comments(limit=None))

    # comments = []
    # for item in subreddit.comments(limit=None):
    #     comments.append(item)

    graph = defaultdict(list)

    for item in comments:
        created = item.created_utc
        t = f"{datetime.fromtimestamp(created)}"
        comments[comments.index(item)] = t
        h = t[11:13]
        graph[h].append(created)

    te = datetime.now() - ts
    if args.debug:
        print(f"{te}\n")

    hours = list(range(24))
    data = []
    for item in hours:
        log = f"Hour: {str(item).zfill(2)} | Comments: {len(graph[str(item).zfill(2)])}"
        data.append(log)

    msg = f"Here are the last {len(comments)} for subreddit `{sname}`, and the frequency of comments for each hour of the day. This is useful for estimating the most active time of day for a subreddit. (i.e. Hour: 00 Comments: 15 would mean there were 15 comments made between midnight and 1 am (UTC))\n"
    dnw = None
    if args.output:
        with open(args.output, 'a') as f:
            f.write(f"\n{msg}")
            for item in data:
                f.write(item+'\n')
    else:
        dnw = True
        print(msg)
        for item in data:
            print(item)
        print("\nWrite data to file? [Y/N]")
        kp = ord(msvcrt.getch())
        if kp == ord('y') or kp == ord('Y'):
            filename = f"{sname}-stats.txt"
            with open(filename, 'w') as f:
                for item in data:
                    f.write(item+'\n')
            print(f"Data wrote to file `{filename}`.")
        else:
            print('Data not written.')
    if dnw is None:
        print('Done.                          ')

def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('subreddit', type=str, help='the subreddit you want stats for')
    parser.add_argument('-o', '--output', type=str, dest='output', help='write to a file, instead of printing to the console')
    parser.add_argument('-S', '--site', default=None, type=str, dest='site', help='a site from your `praw.ini` file')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='for debug purposes (print elapsed time it took to fetch subreddit comments')
    parser.set_defaults(func=substatter)

    args = parser.parse_args(argv)
    args.func(args)
    # main('hackysack', 'numetal')


if __name__ == '__main__':
    sys.exit(main())