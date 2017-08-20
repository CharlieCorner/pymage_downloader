import requests
from bs4 import BeautifulSoup

from exceptions.pymage_exceptions import NotAbleToDownloadException
from models.image import Image
from parsers.base_parser import BaseParser
from utils.utils import tidy_up_url


class Redditupload(BaseParser):
    def get_images(self, post):
        images = []

        html_source = requests.get(post.url).text
        soup = BeautifulSoup(html_source, "lxml")
        match = soup.select("img")

        if not match:
            raise NotAbleToDownloadException("Wasn't able to download %s as the image couldn't be found" % post.url)

        image_url = match[0]["src"]
        image_url = tidy_up_url(image_url) + ".jpg"
        image_file = image_url[image_url.rfind('/') + 1:]

        images.append(Image(image_url, post, image_file))

        return images