import datetime

from utils.utils import limit_file_name, extract_imgur_id_from_url


class BaseImage:

    def __init__(self, post_id: str, url: str, image_filename: str):
        self.post_id = post_id
        self.url = url
        self.image_file = limit_file_name(image_filename)
        self.sub_display_name = None
        self.created = datetime.datetime.now().strftime("%y%m%d")
        self.local_file_name = None


class RedditPostImage(BaseImage):
    _file_name_pattern = "reddit_%s_%s_%s_album_%s_%s_%s"

    def __init__(self, url, post, image_file):
        super().__init__(post.id, url, image_file)

        self.sub_display_name = post.subreddit.display_name
        self.domain = post.domain
        self.created = datetime.datetime.fromtimestamp(post.created).strftime("%y%m%d")

        if "/a/" in post.url or "/gallery/" in post.url:
            self.album_id = extract_imgur_id_from_url(post.url)
        else:
            self.album_id = None

        self.local_file_name = self._file_name_pattern % (
            self.created, self.sub_display_name, self.post_id, self.album_id, self.domain, self.image_file)


class FourChanImage(BaseImage):
    _file_name_pattern = "4chan_%s_%s_%s"

    @staticmethod
    def extract_board_from_url(url: str) -> str:
        # Let's get the first element after the subdomain in the URL
        board = url[url.find("org") + 4:].split("/")[0]
        return board

    def __init__(self, url: str, image_filename: str):
        super().__init__(image_filename[:image_filename.rfind('.')], url, image_filename)
        self.sub_display_name = FourChanImage.extract_board_from_url(url)
        self.local_file_name = self._file_name_pattern % (self.created, self.sub_display_name, self.image_file)
