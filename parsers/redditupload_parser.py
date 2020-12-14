from models.image import RedditPostImage
from parsers.base_parser import BaseParser
from utils.utils import tidy_up_url


class Redditupload(BaseParser):
    def get_images(self, post):
        images = []

        image_url = post.url
        image_file = tidy_up_url(image_url) + ".jpg"
        image_file = image_file[image_file.rfind('/') + 1:]

        images.append(RedditPostImage(image_url, post, image_file))

        return images
