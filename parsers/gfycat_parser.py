from models.image import RedditPostImage
from parsers.base_parser import BaseParser
from utils.utils import *


class Gfycat(BaseParser):
    def get_images(self, post):
        images = []

        # Gfycat links may or may not have a gif, gifv or webm extension, if they don't we can append web
        # (WebM for the win!)
        image_url = tidy_up_url(post.url)

        # A file extension can be 3-4 characters long, let's splice the string and look for the '.'
        if image_url[-5:].rfind('.') < 0:
            image_url = image_url + ".webm"
        # We need to change the URL to giant.gfycat in order to be able to download movies
        gfycat_index = image_url.find("gfycat")
        image_url = image_url[:gfycat_index] + "giant." + image_url[gfycat_index:]

        image_file = image_url[image_url.rfind('/') + 1:]

        images.append(RedditPostImage(image_url, post, image_file))

        return images
