import glob
import logging
import os
from argparse import Namespace

import praw

from downloaders.downloader import Downloader
from exceptions.pymage_exceptions import NotAbleToDownloadException
from parsers.parser_factory import ParserFactory
from utils.utils import download_images

LOGGER = logging.getLogger(__name__)


class RedditDownloader(Downloader):

    REDDIT_FILE_PATTERN = "reddit_*_%s_*"

    def __init__(self):
        super().__init__(RedditDownloader.REDDIT_FILE_PATTERN)

    def download(self, args: Namespace):
        if args.reddit_mode == "user":
            r = praw.Reddit(username=args.user, password=args.password)
        else:
            r = praw.Reddit()

        start_from = args.start_from

        for page in range(0, args.page_limit):
            LOGGER.info("Starting getting posts from page %s" % start_from)
            submissions = self._get_submissions(r, args, start_from)
            self._process_posts(submissions, args)

            next_page = submissions.params["after"]

            # We might get the same next_page as the start_from if the next listing
            #  is less than 25, the default posts per pages coming from PRAW
            if not next_page or next_page is start_from:
                LOGGER.info("No more posts to fetch.")
                break
            start_from = next_page

    def _get_submissions(self, reddit, args, start_from=None):
        params = {"after": start_from}

        if args.reddit_mode == "user":
            if args.should_get_upvoted:
                submissions = reddit.redditor(args.user).upvoted(limit=args.limit, params=params)
            else:
                submissions = reddit.redditor(args.user).saved(limit=args.limit, params=params)
        else:
            subreddit = reddit.subreddit(args.subreddit if isinstance(args.subreddit, str) else "+".join(args.subreddit))

            if args.type == "controversial":
                submissions = subreddit.controversial(time_filter=args.period, limit=args.limit, params=params)
            elif args.type == "new":
                submissions = subreddit.new(limit=args.limit, params=params)
            elif args.type == "top":
                submissions = subreddit.top(time_filter=args.period, limit=args.limit, params=params)
            else:
                submissions = subreddit.hot(limit=args.limit, params=params)

        return submissions

    def _process_posts(self, submissions, args):
        for post in submissions:

            if not isinstance(post, praw.models.Submission) or post.is_self:
                LOGGER.info("Skipping post %s as it is not a submission or is a self post..." % post.id)
                continue

            LOGGER.debug("Post domain: %s" % post.domain)

            pattern_to_search = os.path.join(args.folder, (self.filename_pattern % post.id))
            LOGGER.debug("Pattern to search: %s" % pattern_to_search)

            if not args.should_overwrite and len(glob.glob(pattern_to_search)) > 0:
                LOGGER.info("Skipping post %s, we already have its images..." % post.id)
                continue

            parser = ParserFactory.get_parser(post.url, args)

            if not parser:
                continue

            try:
                images = parser.get_images(post)
                download_images(images, args.folder)
            except NotAbleToDownloadException as e:
                LOGGER.error(e)
        LOGGER.info("The next post ID is: %s" % submissions.params['after'])
