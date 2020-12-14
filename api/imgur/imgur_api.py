import json
import logging
from datetime import datetime

import requests

from api.imgur import *
from exceptions.pymage_exceptions import NotAbleToDownloadException, ImgurAPICommunicationException
from utils.utils import extract_imgur_id_from_url

LOGGER = logging.getLogger(__name__)


class ImgurAPI:

    @staticmethod
    def get_image_urls(url: str) -> list:

        imgur_id = extract_imgur_id_from_url(url)

        try:
            if "/gallery/" in url:
                image_urls = ImgurAPI._get_gallery_urls(imgur_id)

            elif "/a/" in url:
                image_urls = ImgurAPI._get_album_urls(imgur_id)

            else:
                # This is a URL with no gallery, album or extension
                image_urls = ImgurAPI._get_simple_imgur_url(imgur_id)
        except ImgurAPICommunicationException:
            raise NotAbleToDownloadException(f"Couldn't process: {url}")

        return image_urls

    @staticmethod
    def _get_simple_imgur_url(imgur_id: str) -> list:
        imgur_endpoint = ImgurAPI._get_endpoint_url(IMGUR_SIMPLE, imgur_id)

        response = ImgurAPI.get(imgur_endpoint)

        if not response.get("success"):
            raise ImgurAPICommunicationException(f"Unsuccessful query to Imgur API for ID: {imgur_id}")

        link = response.get("data").get("link")

        return [link]

    @staticmethod
    def _get_album_urls(imgur_id: str) -> list:
        imgur_endpoint = ImgurAPI._get_endpoint_url(IMGUR_ALBUM, imgur_id)

        response = ImgurAPI.get(imgur_endpoint)

        if not response.get("success"):
            raise ImgurAPICommunicationException(f"Unsuccessful query to Imgur API for ID: {imgur_id}")

        album_urls = [image_data.get("link") for image_data in response.get("data")]

        return album_urls

    @staticmethod
    def _get_gallery_urls(imgur_id: str) -> list:
        imgur_endpoint = ImgurAPI._get_endpoint_url(IMGUR_GALLERY, imgur_id)

        response = ImgurAPI.get(imgur_endpoint)

        if not response.get("success"):
            raise ImgurAPICommunicationException(f"Unsuccessful query to Imgur API for ID: {imgur_id}")

        gallery_urls = [image_data.get("link") for image_data in response.get("data").get("images")]

        return gallery_urls

    @staticmethod
    def _get_endpoint_url(endpoint: str, imgur_id: str) -> str:
        return IMGUR_ENDPOINTS.get(endpoint).replace(IMGUR_ID_URL_PLACEHOLDER, imgur_id)

    @staticmethod
    def _update_api_limits(response: requests.models.Response):
        reported_user_limit = int(response.headers[IMGUR_API_RESPONSE_HEADER_USER_LIMIT])
        reported_user_remaining = int(response.headers[IMGUR_API_RESPONSE_HEADER_USER_REMAINING])
        reported_user_reset_ts = int(response.headers[IMGUR_API_RESPONSE_HEADER_USER_RESET])

        LOGGER.debug(f"Imgur API Remaining calls: {reported_user_remaining}")
        LOGGER.debug(f"Imgur API Next Limit Reset Timestamp: {reported_user_reset_ts}")

        IMGUR_PARAMS[IMGUR_PARAMS_API_CALLS_LIMITS][IMGUR_PARAMS_API_CALLS_LIMITS_USER_LIMIT] \
            = reported_user_limit
        IMGUR_PARAMS[IMGUR_PARAMS_API_CALLS_LIMITS][IMGUR_PARAMS_API_CALLS_LIMITS_USER_REMAINING] \
            = reported_user_remaining
        IMGUR_PARAMS[IMGUR_PARAMS_API_CALLS_LIMITS][IMGUR_PARAMS_API_CALLS_LIMITS_USER_RESET_TIMESTAMP] \
            = reported_user_reset_ts

    @staticmethod
    def _check_api_limits():
        # This limits need to be checked according to the Imgur API docs https://apidocs.imgur.com/
        # HTTP Header	Description
        # X-RateLimit-UserLimit	Total credits that can be allocated.
        # X-RateLimit-UserRemaining	Total credits available.
        # X-RateLimit-UserReset	Timestamp (unix epoch) for when the credits will be reset.
        # X-RateLimit-ClientLimit	Total credits that can be allocated for the application in a day.
        # X-RateLimit-ClientRemaining	Total credits remaining for the application in a day.
        remaining_calls = IMGUR_PARAMS[IMGUR_PARAMS_API_CALLS_LIMITS][IMGUR_PARAMS_API_CALLS_LIMITS_USER_REMAINING]
        reset_timestamp = IMGUR_PARAMS[IMGUR_PARAMS_API_CALLS_LIMITS][IMGUR_PARAMS_API_CALLS_LIMITS_USER_RESET_TIMESTAMP]

        if remaining_calls <= IMGUR_LIMIT_WARNING_THRESHOLD:
            LOGGER.warning(f"Approaching the limit of calls allowed for the Imgur API, remaining: {remaining_calls}")
        elif remaining_calls <= 0:
            readable_reset_time = datetime.utcfromtimestamp(reset_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            raise ImgurAPICommunicationException(f"The limit of calls to the Imgur API has been reached, "
                                                 f"more call will be available at {readable_reset_time}")

    @staticmethod
    def get(endpoint: str, headers: dict = {}) -> dict:

        # The Imgur Client ID must be set before we can do anything else
        if not IMGUR_PARAMS.get(IMGUR_PARAMS_CLIENT_ID):
            raise ImgurAPICommunicationException(f"The Client ID for the Imgur API is not set! Skipping {endpoint}")

        # The following will throw an Exception if the limits have been met and will prevent any further call to be made
        #  to the Imgur API
        ImgurAPI._check_api_limits()

        # Add the Imgur API Client ID to the Authorization HTTP Header
        if HTTP_HEADER_AUTHORIZATION not in headers:
            headers[HTTP_HEADER_AUTHORIZATION] = f"Client-ID {IMGUR_PARAMS.get(IMGUR_PARAMS_CLIENT_ID)}"

        try:
            LOGGER.debug(f"Querying API Imgur on {endpoint}...")

            with requests.get(endpoint, headers=headers) as response:
                if response.ok:
                    LOGGER.info('Imgur API query successful!')
                    ImgurAPI._update_api_limits(response)
                    data = json.loads(response.text)
                    return data

                else:
                    raise ImgurAPICommunicationException(
                        f"Failed to download, we got an HTTP {response.status_code} error "
                        f"saying {response.text} for {endpoint}")

        except requests.exceptions.ConnectionError as ex:
            LOGGER.error(ex)
            raise ImgurAPICommunicationException(f"Couldn't connect to {endpoint}, because of {str(ex)}")

# Sample Imgur Response
# {
        #     "data": {
        #         "id": "7W1xjas",
        #         "title": null,
        #         "description": null,
        #         "datetime": 1541129695,
        #         "type": "image/jpeg",
        #         "animated": false,
        #         "width": 640,
        #         "height": 691,
        #         "size": 123980,
        #         "views": 29125,
        #         "bandwidth": 3610917500,
        #         "vote": null,
        #         "favorite": false,
        #         "nsfw": true,
        #         "section": "hentai",
        #         "account_url": null,
        #         "account_id": null,
        #         "is_ad": false,
        #         "in_most_viral": false,
        #         "has_sound": false,
        #         "tags": [],
        #         "ad_type": 0,
        #         "ad_url": "",
        #         "in_gallery": false,
        #         "link": "https://i.imgur.com/7W1xjas.jpg"
        #     },
        #     "success": true,
        #     "status": 200
        # }