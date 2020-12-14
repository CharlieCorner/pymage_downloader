from models.image import RedditPostImage
from parsers.base_parser import BaseParser


class IReddIt(BaseParser):
    def get_images(self, post):
        images = []

        image_file = post.url[post.url.rfind('/') + 1:]

        images.append(RedditPostImage(post.url, post, image_file))

        return images
