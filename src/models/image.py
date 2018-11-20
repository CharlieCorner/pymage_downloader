import datetime
from utils.utils import limit_file_name


class Image:
    _file_name_pattern = "reddit_%s_%s_%s_album_%s_%s_%s"

    def __init__(self, url, post, image_file):
        self.post_id = post.id
        self.url = url
        self.sub_display_name = post.subreddit.display_name
        self.image_file = limit_file_name(image_file)
        self.domain = post.domain
        self.created = datetime.datetime.fromtimestamp(post.created).strftime("%y%m%d")

        if "/a/" in post.url:
            self.album_id = post.url[post.url.index("/a/") + 3:]
        elif "/gallery/" in post.url:
            self.album_id = post.url[post.url.index("/gallery/") + 9:]
        else:
            self.album_id = None

        self.local_file_name = self._file_name_pattern % (
            self.created, self.sub_display_name, self.post_id, self.album_id, self.domain, self.image_file)
