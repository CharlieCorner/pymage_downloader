import logging
import re

import requests
from bs4 import BeautifulSoup

from exceptions.pymage_exceptions import NotAbleToDownloadException
from models.image import Image
from parsers.base_parser import BaseParser
from utils.utils import *

LOGGER = logging.getLogger(__name__)


class ImgurParser(BaseParser):
    def __init__(self) -> None:
        self._imgur_url_pattern = re.compile(r"(imgur.com/(.*))(\?.*)?")

    def get_images(self, post):
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
                image_url = m['src']
                image_url = tidy_up_url(image_url)
                image_file = image_url[image_url.rfind('/') + 1:]
                images.append(Image(image_url, post, image_file))

        elif tidy_up_url(post.url)[post.url.rfind(".") + 1:] in ["jpeg", "png", "jpg", "gif", "gifv"]:
            # This is a direct url
            image_url = tidy_up_url(post.url)

            if image_url.endswith("gifv"):
                image_url = image_url.replace("gifv", "mp4")

            image_file = image_url[image_url.rfind('/') + 1:]

            images.append(Image(image_url, post, image_file))

        elif "imgur.com/" in post.url:
            # This is an Imgur page with a single image

            html_source = requests.get(post.url).text
            soup = BeautifulSoup(html_source, "lxml")
            match = soup.select("a.zoom")

            if not match:
                match = soup.select("img.post-image-placeholder")

                if not match:
                    match = soup.select("img")

                image_url = match[0]['src']

            else:
                image_url = match[0]["href"]

            image_url = tidy_up_url(image_url)
            image_file = image_url[image_url.rfind('/') + 1:]

            images.append(Image(image_url, post, image_file))
        else:
            raise NotAbleToDownloadException("Couldn't process %s" % post.url)

        return images
