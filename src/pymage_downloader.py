#!/usr/bin/python3

import logging
import sys

from argparsers import parse_args
from downloaders.downloader_factory import DownloaderFactory
from downloaders.reddit import reddit_downloader
from utils.utils import prepare_download_folder

LOGGER = logging.getLogger(__name__)


def main():
    args = parse_args()
    configure_logging(args.is_debug)
    prepare_download_folder(args.folder)

    if args.site == "reddit":
        reddit_downloader(args)

    else:
        downloader = DownloaderFactory.get_downloader(args)

        if not downloader:
            raise NotImplementedError("No suitable downloader was found!")

        downloader.download(args)


def configure_logging(is_debug=False):
    log_format = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
    logging.basicConfig(format=log_format,
                        filename='pymage.log',
                        level=logging.DEBUG if is_debug else logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)

    LOGGER.info("******* Pymage Downloader *******")
    LOGGER.debug("Ready to DEBUG!")


if __name__ == '__main__':
    main()
