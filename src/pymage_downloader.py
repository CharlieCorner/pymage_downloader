#!/usr/bin/python3

import glob
import logging
import os
import sys
from argparse import ArgumentParser

import praw
import requests

from exceptions.pymage_exceptions import NotAbleToDownloadException
from parsers.parser_factory import ParserFactory

LOGGER = logging.getLogger(__name__)
VERSION = "0.0.1"


def main():
    args = _parse_args()
    configure_logging(args.is_debug)
    prepare_download_folder(args.folder)

    if args.user:
        r = praw.Reddit(username=args.user, password=args.password)
    else:
        r = praw.Reddit()

    submissions = get_submissions(r, args)

    process_posts(submissions, args)


def get_submissions(reddit, args):

    if args.user:
        if args.should_get_upvoted:
            submissions = reddit.redditor(args.user).upvoted(limit=args.limit)
        else:
            submissions = reddit.redditor(args.user).saved(limit=args.limit)
    else:
        subreddit = reddit.subreddit(args.subreddit)

        if args.type == "controversial":
            submissions = subreddit.controversial(time_filter=args.period, limit=args.limit)
        elif args.type == "new":
            submissions = subreddit.new(limit=args.limit)
        elif args.type == "top":
            submissions = subreddit.top(time_filter=args.period, limit=args.limit)
        else:
            submissions = subreddit.hot(limit=args.limit)

    return submissions


def process_posts(submissions, args):
    for post in submissions:
        LOGGER.debug("Post domain: %s" % post.domain)

        pattern_to_search = os.path.join(args.folder, ("reddit_*_%s_*" % post.id))
        LOGGER.debug("Pattern to search: %s" % pattern_to_search)

        if not args.should_overwrite and len(glob.glob(pattern_to_search)) > 0:
            LOGGER.info("Skipping post %s, we already have its images..." % post.id)
            continue

        parser = ParserFactory.get_parser(post.url)

        if not parser:
            LOGGER.warning("The domain in %s is not supported..." % post.url)
            continue

        try:
            images = parser.get_images(post)
            download_images(images, args.folder)
        except NotAbleToDownloadException as e:
            LOGGER.error(e)
    LOGGER.debug("The next ID is: %s" % submissions.params['after'])


def download_images(images, folder):
    for i in images:
        LOGGER.info('Downloading %s...' % i.url)
        response = requests.get(i.url)

        if response.status_code == 200:
            file_name = os.path.join(folder, i.local_file_name)
            LOGGER.info('Saving %s...' % file_name)

            with open(file_name, 'wb') as fo:
                for chunk in response.iter_content(4096):
                    fo.write(chunk)

            response.close()

        else:
            response.close()
            raise NotAbleToDownloadException(
                "Failed to download, we got an HTTP %i error for %s" % (response.status_code, i.url))


def prepare_download_folder(folder):
    if not os.path.exists(folder):
        LOGGER.debug("Creating folder %s" % folder)
        os.makedirs(folder)


def _parse_args():
    """Parse args with argparse
    :returns: args
    """
    parser = ArgumentParser(description="Pymage Downloader %s - Download pics from subreddit posts" % VERSION)

    parser.add_argument('--subreddit', '-s',
                        default='pics',
                        # nargs='+', #TODO implement functionality for more than one subreddit
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
                        default=100,
                        help="Maximum URL limit per subreddit.")

    parser.add_argument('--destination', '-d',
                        dest='folder',
                        default='reddit_pics',
                        help="Defines a download folder.")

    parser.add_argument("--overwrite", "-o",
                        dest="should_overwrite",
                        action="store_true",
                        help="Specifies if files should be overwritten if they were already downloaded.")

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

    # TODO Add pagination limit
    # TODO Add argument to start from a particular post on

    args = parser.parse_args()

    if args.user and not args.password:
        parser.error("A user was specified but a password was not, please provide complete credentials.")

    return args


def configure_logging(is_debug=False):
    log_format = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
    logging.basicConfig(format=log_format,
                        filename='pymage.log',
                        level=logging.DEBUG if is_debug else logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(logging.DEBUG)
    LOGGER.addHandler(console_handler)

    LOGGER.info("******* Pymage Downloader *******")
    LOGGER.debug("Ready to DEBUG!")


if __name__ == '__main__':
    main()
