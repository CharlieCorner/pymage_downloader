from parsers import deviantart_parser
from parsers import direct_parser
from parsers import gfycat_parser
from parsers import imgur_parser
from parsers import instagram_parser
from parsers import ireddit_parser
from parsers import redditupload_parser

from utils.utils import *

LOGGER = logging.getLogger(__name__)


class ParserFactory:
    _PARSERS = {
        "imgur": imgur_parser.ImgurParser(),
        "redd.it": ireddit_parser.IReddIt(),
        "gfycat": gfycat_parser.Gfycat(),
        "direct_image": direct_parser.DirectFile(),
        "deviantart": deviantart_parser.Deviantart(),
        "instagram": instagram_parser.Instagram(),
        "redditupload": redditupload_parser.Redditupload()
    }

    @staticmethod
    def get_parser(url):
        parser = None

        if not url:
            raise ValueError("No URL was specified")

        if tidy_up_url(url)[url.rfind(".") + 1:] in ["jpeg", "png", "jpg", "gif", "gifv", "webm", "mp4"]:
            LOGGER.debug("Chooosing the direct_image parser")
            return ParserFactory._PARSERS["direct_image"]

        for key in ParserFactory._PARSERS:
            if key in url:
                LOGGER.debug("Choosing the %s parser" % key)
                return ParserFactory._PARSERS[key]

        return parser
