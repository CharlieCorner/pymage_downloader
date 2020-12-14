import logging
from argparse import Namespace

from downloaders import downloader
from downloaders.downloader import Downloader
from downloaders.reddit_downloader import RedditDownloader

LOGGER = logging.getLogger(__name__)

FOURCHAN_FILE_PATTERN = "4chan*_%s.*"
IMGUR_SITE_FILE_PATTERN = "imgur*_%s.*"


class DownloaderFactory:

    _DOWNLOADERS = {
        "imgur": Downloader(IMGUR_SITE_FILE_PATTERN),
        "4chan": Downloader(FOURCHAN_FILE_PATTERN),
        "reddit": RedditDownloader()
    }

    @staticmethod
    def get_downloader(args: Namespace) -> downloader.Downloader:

        downloader = None

        # We don't need to parse anything for reddit, so we can just return the Downloader
        if args.site == "reddit":
            return DownloaderFactory._DOWNLOADERS.get("reddit")

        if not args.url:
            raise ValueError("No URL was specified")

        for key in DownloaderFactory._DOWNLOADERS:

            if key in args.url:

                LOGGER.debug(f"Choosing the {key} downloader")
                return DownloaderFactory._DOWNLOADERS[key]

        if not downloader:
            LOGGER.warning("The domain in %s is not supported..." % args.url)

        return downloader
