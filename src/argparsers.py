from argparse import ArgumentParser

VERSION = "2.0.0"


def parse_args():
    """Parse args with argparse
    :returns: args
    """
    parser = ArgumentParser(description=f"Pymage Downloader {VERSION} - Download pics from different sites")

    build_site_subparsers(parser)

    parser.add_argument('--destination', '-d',
                        dest='folder',
                        default='pymage_pics',
                        help="Defines a download folder.")

    parser.add_argument("--overwrite", "-o",
                        dest="should_overwrite",
                        action="store_true",
                        help="Specifies if files should be overwritten if they were already downloaded.")

    parser.add_argument("--debug",
                        dest="is_debug",
                        action="store_true",
                        help="Activates debug mode.")

    args = parser.parse_args()

    if args.site == "reddit":

        if args.start_from and not args.start_from.startswith("t3_"):
            args.start_from = "t3_" + args.start_from

    return args


def build_site_subparsers(parser: ArgumentParser):
    site_subparsers = parser.add_subparsers(title='Sites',
                                            description="Choose from which site you'd like to download images",
                                            help='supported sites',
                                            dest="site")
    site_subparsers.required = True

    reddit_subparser(site_subparsers)
    url_parser(site_subparsers)


def reddit_subparser(site_subparsers):
    reddit_argparser = site_subparsers.add_parser('reddit')

    reddit_modes = reddit_argparser.add_subparsers(title='Reddit Modes',
                                                   description="Choose if you'd like to manipulate a subreddit "
                                                               "or a user's posts",
                                                   dest="reddit_mode",
                                                   help='reddit modes')

    # General options for Reddit
    reddit_argparser.add_argument('--limit', '-l',
                                  metavar='N',
                                  type=int,
                                  default=25,
                                  help="Maximum URL limit per subreddit.")

    reddit_argparser.add_argument("--imgur-html", "-ih",
                                  dest="should_parse_imgur_html",
                                  action="store_true",
                                  help="Forces the use of the deprecated Imgur HTML parser "
                                       "instead of the Imgur API Parser.")

    reddit_argparser.add_argument('--page-limit', '-pl',
                                  dest="page_limit",
                                  metavar='N',
                                  type=int,
                                  default=4,
                                  help="Maximum amount of pages to get.")

    reddit_argparser.add_argument('--start-from', '-sf',
                                  dest="start_from",
                                  metavar='ID',
                                  help="Post ID from which to get a listing.")

    # Subreddit mode
    subreddit_mode = reddit_modes.add_parser("subreddit",
                                             description="Manipulate subreddits posts",
                                             help='subreddit options')
    subreddit_mode.add_argument('subreddit',
                                nargs='+',
                                metavar="SUBREDDITS",
                                help="List of the subreddits.")

    subreddit_mode.add_argument('--period', '-p',
                                default='week',
                                choices=['hour', 'day', 'week', 'month', 'year', 'all'],
                                help="[h]our, [d]ay, [w]eek, [m]onth, [y]ear, or [a]ll. Period "
                                     "of time from which you want images. Only works for top and controversial")

    subreddit_mode.add_argument('--type', '-t',
                                default='hot',
                                choices=['hot', 'top', 'new', 'controversial'],
                                help="[hot], [top], [new], [controversial]. Type of listing of posts "
                                     "in a subreddit.")

    # User mode
    user_mode = reddit_modes.add_parser("user",
                                        description="Manipulate a user's posts",
                                        help='user options')
    user_mode.add_argument("user",
                           help="Specifies the user name.")

    user_mode.add_argument("password",
                           default="",
                           help="Specifies the user name.")

    user_mode.add_argument("--upvoted",
                           dest="should_get_upvoted",
                           action="store_true",
                           help="Specifies if the upvoted posts of a user should be fetched. Otherwise, "
                                "get the saved ones.")


def url_parser(site_subparsers):
    url_argparser = site_subparsers.add_parser('url')
    url_argparser.add_argument('url',
                               metavar="URL",
                               help="The URL from which to download images.")

