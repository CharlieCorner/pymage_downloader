from argparse import ArgumentParser

VERSION = "2.0.0"


def parse_args():
    """Parse args with argparse
    :returns: args
    """
    parser = ArgumentParser(description=f"Pymage Downloader {VERSION} - Download pics from different sites")

    parser.add_argument('--site',
                        default='reddit',
                        choices=['reddit', '4chan'],
                        help="Choose from which site you'd like to download images")

    parser.add_argument('--url',
                        help="If the 4chan downloader was selected, the url of the thread to parse.")

    parser.add_argument('--subreddit', '-s',
                        default='pics',
                        nargs='+',
                        help="Name of the subreddit.")

    parser.add_argument('--period', '-p',
                        default='week',
                        choices=['hour', 'day', 'week', 'month', 'year', 'all'],
                        help="[h]our, [d]ay, [w]eek, [m]onth, [y]ear, or [a]ll. Period "
                             "of time from which you want images. Only works for top and controversial")

    parser.add_argument('--type', '-t',
                        default='hot',
                        choices=['hot', 'top', 'new', 'controversial'],
                        help="[hot], [top], [new], [controversial]. Type of listing of posts "
                             "in a subreddit.")

    parser.add_argument('--limit', '-l',
                        metavar='N',
                        type=int,
                        default=25,
                        help="Maximum URL limit per subreddit.")

    parser.add_argument('--destination', '-d',
                        dest='folder',
                        default='reddit_pics',
                        help="Defines a download folder.")

    parser.add_argument("--overwrite", "-o",
                        dest="should_overwrite",
                        action="store_true",
                        help="Specifies if files should be overwritten if they were already downloaded.")

    parser.add_argument("--imgur-html", "-ih",
                        dest="should_parse_imgur_html",
                        action="store_true",
                        help="Forces the use of the deprecated Imgur HTML parser instead of the Imgur API Parser.")

    parser.add_argument("--debug",
                        dest="is_debug",
                        action="store_true",
                        help="Activates debug mode.")

    parser.add_argument("--user", "-u",
                        dest="user",
                        help="Specifies the user name. This overrides the subreddit option.")

    parser.add_argument("--pass", "-w",
                        dest="password",
                        help="Specifies the user name. Required if '-u' is specified.")

    parser.add_argument("--upvoted",
                        dest="should_get_upvoted",
                        action="store_true",
                        help="Specifies if the upvoted posts of a user should be fetched. Otherwise, get the saved "
                             "ones.")

    parser.add_argument('--page-limit', '-pl',
                        dest="page_limit",
                        metavar='N',
                        type=int,
                        default=4,
                        help="Maximum amount of pages to get.")

    parser.add_argument('--start-from', '-sf',
                        dest="start_from",
                        metavar='ID',
                        help="Post ID from which to get a listing.")

    args = parser.parse_args()

    if args.site == "reddit":

        if args.user and not args.password:
            parser.error("A user was specified but a password was not, please provide complete credentials.")

        if args.start_from and not args.start_from.startswith("t3_"):
            args.start_from = "t3_" + args.start_from

    elif args.site == "4chan":

        if not args.url:
            parser.error("4chan mode selected, but no URL for the 4chan thread was provided.")

    return args