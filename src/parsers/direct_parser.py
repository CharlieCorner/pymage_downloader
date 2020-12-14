from models.image import RedditPostImage
from parsers.base_parser import BaseParser
from utils.utils import tidy_up_url


class DirectFile(BaseParser):
    def get_images(self, post):
        images = []

        post_url = tidy_up_url(post.url)

        image_file = post_url[post_url.rfind('/') + 1:]

        images.append(RedditPostImage(post_url, post, image_file))

        return images
