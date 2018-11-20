from models.image import Image
from utils.utils import tidy_up_url


class ImgurAPI:
    _IMGUR_PARAMS = {
        "client_id": "",
        "api_calls_limits": {
            "user_limit": -1,
            "user_remaining": -1,
            "user_reset_timestamp": -1,
            "client_limit": -1,
            "client_remaining": -1
        }
    }

    def __init__(self):
        pass

    @staticmethod
    def get_image_urls(post: dict) -> list:
        url = tidy_up_url(post.get("url"))
        imgur_id = url[url.rfind("/") + 1:]

        if "/gallery/" in url:
            image_urls = ImgurAPI._get_gallery_urls(imgur_id)

        elif "/a/" in url:
            image_urls = ImgurAPI._get_album_urls(imgur_id)

        else:
            # This is a URL with no gallery, album or extension
            image_urls = ImgurAPI._get_simple_imgur_url(imgur_id)

        return image_urls

    @staticmethod
    def _get_simple_imgur_url(imgur_id: str) -> list:
        raise NotImplementedError

    @staticmethod
    def _get_album_urls(imgur_id: str) -> list:
        raise NotImplementedError

    @staticmethod
    def _get_gallery_urls(imgur_id: str) -> list:
        raise NotImplementedError


