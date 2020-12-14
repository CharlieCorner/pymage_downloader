import requests
from bs4 import BeautifulSoup

from exceptions.pymage_exceptions import NotAbleToDownloadException
from models.image import FourChanImage
from parsers.base_parser import BaseParser
from utils.utils import tidy_up_url, get_file_name_from_url

IMAGES_CSS_SELECTOR = "a.fileThumb"


class FourChan(BaseParser):
    def get_images(self, url: str):
        images = []

        html_source = requests.get(url).text

        soup = BeautifulSoup(html_source, "lxml")

        matches = soup.select(IMAGES_CSS_SELECTOR)

        if not matches:
            raise NotAbleToDownloadException(f"Couldn't process {url}")

        for m in matches:
            image_url = tidy_up_url(m['href'])
            image_filename = get_file_name_from_url(image_url)
            images.append(FourChanImage(image_url, image_filename))

        return images
