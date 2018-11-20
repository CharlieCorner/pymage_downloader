import re
from abc import abstractmethod

import requests
from bs4 import BeautifulSoup

from api.imgur.imgur_api import ImgurAPI
from exceptions.pymage_exceptions import NotAbleToDownloadException
from models.image import Image
from parsers.base_parser import BaseParser
from utils.utils import *

LOGGER = logging.getLogger(__name__)


class ImgurBaseParser(BaseParser):

    @abstractmethod
    def get_images(self, post):
        raise NotImplementedError("A concrete parser must be used")

    @staticmethod
    def is_imgur_direct_url(url: str) -> bool:
        return tidy_up_url(url)[url.rfind(".") + 1:] in ["jpeg", "png", "jpg", "gif", "gifv"]

    @staticmethod
    def get_image_from_direct_url(post: dict) -> Image:
        image_url = tidy_up_url(post.get("url"))

        if image_url.endswith("gifv"):
            image_url = image_url.replace("gifv", "mp4")

        image_file = ImgurBaseParser.get_file_name_from_url(image_url)

        image = Image(image_url, post, image_file)

        return image

    @staticmethod
    def get_file_name_from_url(url: str) -> str:
        return url[url.rfind('/') + 1:]


class ImgurParser(ImgurBaseParser):
    def __init__(self) -> None:
        self._imgur_url_pattern = re.compile(r"(imgur.com/(.*))(\?.*)?")

    def get_images(self, post) -> list:
        images = []

        if "/a/" in post.url or "/gallery/" in post.url:
            # This is an album submission

            html_source = requests.get(post.url).text

            soup = BeautifulSoup(html_source, "lxml")
            matches = soup.select('img.post-image-placeholder')
            
            if not matches:
                matches = soup.select("img[itemprop]")

            if not matches:
                raise NotAbleToDownloadException("Couldn't process %s" % post.url)

            for m in matches:
                image_url = tidy_up_url(m['src'])
                image_file = ImgurBaseParser.get_file_name_from_url(image_url)
                images.append(Image(image_url, post, image_file))

        elif ImgurParser.is_imgur_direct_url(post.get("get")):
            # This is a direct url
            images.append(ImgurParser.get_image_from_direct_url(post))

        elif "imgur.com/" in post.url:
            # This is an Imgur page with a single image

            html_source = requests.get(post.url).text
            soup = BeautifulSoup(html_source, "lxml")
            match = soup.select("a.zoom")

            if match:
                image_url = match[0]["href"]
            else:
                match = soup.select("img.post-image-placeholder")

                if not match:
                    match = soup.select("img[itemprop]")
                if not match:
                    match = soup.select("img")
                if not match:
                    raise NotAbleToDownloadException("Couldn't process %s" % post.url)

                image_url = match[0]['src']

            image_url = tidy_up_url(image_url)
            image_file = ImgurParser.get_file_name_from_url(image_url)

            images.append(Image(image_url, post, image_file))
        else:
            raise NotAbleToDownloadException("Couldn't process %s" % post.url)

        return images


class ImgurAPIParser(ImgurBaseParser):

    def get_images(self, post: dict) -> list:
        # First check if it is a direct URL so that we avoid querying the API
        if ImgurAPIParser.is_imgur_direct_url(post.get("url")):
            return [ImgurAPIParser.get_image_from_direct_url(post)]

        urls = ImgurAPI.get_image_urls(post)
        image_entities = []

        for u in urls:
            image_entities.append(Image(u, post, ImgurAPIParser.get_file_name_from_url(u)))

        return image_entities
