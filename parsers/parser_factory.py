from parsers import base_parser, fourchan_parser
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
        "imgur": imgur_parser.ImgurAPIParser(),
        "imgurhtml": imgur_parser.ImgurHTMLParser(),
        "redd.it": ireddit_parser.IReddIt(),
        "gfycat": gfycat_parser.Gfycat(),
        "direct_image": direct_parser.DirectFile(),
        "deviantart": deviantart_parser.Deviantart(),
        "instagram": instagram_parser.Instagram(),
        "redditupload": redditupload_parser.Redditupload(),
        "4chan": fourchan_parser.FourChan()
    }

    @staticmethod
    def get_parser(url: str, args=None) -> base_parser.BaseParser:
        parser = None

        if not url:
            raise ValueError("No URL was specified")

        # Gifv links, although they are direct links, when hosted in imgur, they work as differently and need to be
        #  converted to MP4 before attempting to download them, so we'll not use the direct parser for those and let the
        #  domain determine the parser
        if tidy_up_url(url)[url.rfind(".") + 1:] in ["jpeg", "png", "jpg", "gif", "webm", "mp4"]:
            LOGGER.debug("Chooosing the direct_image parser")
            return ParserFactory._PARSERS["direct_image"]

        for key in ParserFactory._PARSERS:

            if key in url:

                # This will allow us to support more than one parser for a given domain and control it through an arg
                if key == "imgur" and args and args.should_parse_imgur_html:
                    LOGGER.debug("Choosing the Imgur HTML Parser")
                    return ParserFactory._PARSERS["imgurhtml"]

                LOGGER.debug(f"Choosing the {key} parser")
                return ParserFactory._PARSERS[key]

        if not parser:
            LOGGER.warning("The domain in %s is not supported..." % url)

        return parser
