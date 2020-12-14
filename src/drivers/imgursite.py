import glob
import logging
import os
from argparse import Namespace

from exceptions.pymage_exceptions import NotAbleToDownloadException
from parsers.parser_factory import ParserFactory
from utils.utils import download_images

LOGGER = logging.getLogger(__name__)


def imgursite_downloader(args: Namespace):

    LOGGER.info(f"Downloading images from {args.url}...")
    # Get the Imgur parser
    parser = ParserFactory.get_parser(args.url)

    try:
        images = parser.get_images(args.url)
        images = filter_existent_images(images, args)
        download_images(images, args.folder)
    except NotAbleToDownloadException as e:
        LOGGER.error(e)

    LOGGER.info("The Imgur downloader is done")


def filter_existent_images(images, args) -> list:
    new_images = []

    for i in images:

        pattern_to_search = os.path.join(args.folder, ("*_%s*" % i.post_id))
        LOGGER.debug("Pattern to search: %s" % pattern_to_search)

        if not args.should_overwrite and len(glob.glob(pattern_to_search)) > 0:
            LOGGER.info(f"Skipping post {i.post_id}, we already have its images...")
            continue
        new_images.append(i)

    return new_images