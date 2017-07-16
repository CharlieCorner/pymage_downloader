import logging

LOGGER = logging.getLogger(__name__)


def tidy_up_url(url):
    if url.startswith("//"):
        # If no protocol was supplied, add https
        url = "https:" + url

    if '?' in url:
        url = url[:url.rfind('?')]
    return url


def limit_file_name(file_name, length=65):
    if len(file_name) <= length:
        return file_name
    else:
        extension = file_name[file_name.rfind("."):]
        file_name = file_name[:length - len(extension)] + extension
        LOGGER.debug("Will have to limit the file name %s as it exceeds %i" % (file_name, length))
        return file_name
