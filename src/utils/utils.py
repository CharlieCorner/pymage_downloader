import logging
import os

import requests

from exceptions.pymage_exceptions import NotAbleToDownloadException

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


def download_images(images, folder):
    for i in images:
        LOGGER.info('Downloading %s...' % i.url)

        try:
            with requests.get(i.url) as response:
                if response.ok:
                    file_name = os.path.join(folder, i.local_file_name)
                    LOGGER.info('Saving %s...' % file_name)

                    with open(file_name, 'wb') as fo:
                        for chunk in response.iter_content(4096):
                            fo.write(chunk)

                else:
                    raise NotAbleToDownloadException(
                        "Failed to download, we got an HTTP %i error for %s" % (response.status_code, i.url))

        except requests.exceptions.ConnectionError as ex:
            LOGGER.error(ex)
            raise NotAbleToDownloadException("Couldn't connect to %s, because of %s" % (i.url, str(ex)))


def prepare_download_folder(folder):
    if not os.path.exists(folder):
        LOGGER.debug("Creating folder %s" % folder)
        os.makedirs(folder)
