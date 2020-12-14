import glob
import logging
import os
from abc import abstractmethod
from argparse import Namespace

from exceptions.pymage_exceptions import NotAbleToDownloadException
from parsers.parser_factory import ParserFactory
from utils.utils import download_images

LOGGER = logging.getLogger(__name__)


class Downloader:

    def __init__(self, filename_pattern: str):

        if "%s" not in filename_pattern:
            raise ValueError("'%s' placeholder not found in filename_pattern and it is needed for duplicate detection.")

        self.filename_pattern = filename_pattern

        self.parser = None
        self.args = None

    @abstractmethod
    def download(self, args: Namespace):

        self.args = args
        self.parser = ParserFactory.get_parser(args.url)

        if not self.parser:
            raise NotImplementedError(f"No parser was found to download from {args.url}")

        LOGGER.info(f"Downloading images from {self.args.url}")

        try:
            images = self.parser.get_images(self.args.url)
            images = self._filter_existent_images(images)
            download_images(images, self.args.folder)

        except NotAbleToDownloadException as e:
            LOGGER.error(e)

        LOGGER.info("The downloader is done!")

    @abstractmethod
    def _filter_existent_images(self, images: list) -> list:
        new_images = []

        for i in images:

            pattern_to_search = self.filename_pattern % i.post_id
            pattern_to_search = os.path.join(self.args.folder, pattern_to_search)
            LOGGER.debug("Pattern to search: %s" % pattern_to_search)

            if not self.args.should_overwrite and len(glob.glob(pattern_to_search)) > 0:
                LOGGER.info(f"Skipping post {i.post_id}, we already have its images...")
                continue
            new_images.append(i)

        return new_images
