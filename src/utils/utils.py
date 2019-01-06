import logging

LOGGER = logging.getLogger(__name__)


def extract_imgur_id_from_url(url: str) -> str:
    url = tidy_up_url(url)
    imgur_id = url[url.rfind("/") + 1:]

    return imgur_id


def tidy_up_url(url: str) -> str:
    if url.startswith("//"):
        # If no protocol was supplied, add https
        url = "https:" + url

    if '?' in url:
        url = url[:url.rfind('?')]

    if url.endswith("/"):
        url = url[:-1]
    return url


def limit_file_name(file_name: str, length: int = 65) -> str:
    if len(file_name) <= length:
        return file_name
    else:
        extension = file_name[file_name.rfind("."):]
        file_name = file_name[:length - len(extension)] + extension
        LOGGER.debug("Will have to limit the file name %s as it exceeds %i" % (file_name, length))
        return file_name
