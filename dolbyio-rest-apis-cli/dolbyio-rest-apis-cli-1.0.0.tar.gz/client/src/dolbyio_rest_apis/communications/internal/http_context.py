"""
dolbyio_rest_apis.communications.internal.helpers
~~~~~~~~~~~~~~~

This module contains internal helpers.
"""

from aiohttp import BasicAuth, ClientResponse, ContentTypeError
from dolbyio_rest_apis.core.http_context import HttpContext
from dolbyio_rest_apis.core.helpers import get_value_or_default
from dolbyio_rest_apis.core.http_request_error import HttpRequestError
import json
from sty import fg
from typing import Any, Dict, List

class CommunicationsHttpContext(HttpContext):
    """HTTP Context class for Communications APIs"""

    async def requests_post(
            self,
            access_token: str,
            url: str,
            payload: Any=None,
        ) -> Any or None:
        r"""
        Sends a POST request.

        Args:
            access_token: The Access Token to use for authentication.
            url: Where to send the request to.
            payload: (Optional) Content of the request.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        if payload is None:
            payload = '{}' # The REST APIs don't support an empty payload
        else:
            payload = json.dumps(payload, indent=4)

        return await self._send_request(
            method='POST',
            url=url,
            headers=headers,
            data=payload,
        )

    async def requests_post_basic_auth(
            self,
            consumer_key: str,
            consumer_secret: str,
            url: str,
            json_payload: str=None,
            data: Dict[str, Any]=None,
        ) -> Any or None:
        r"""
        Sends a POST request with Basic authentication.

        Args:
            consumer_key: The Dolby.io Consumer Key.
            consumer_secret: The Dolby.io Consumer Secret.
            url: Where to send the request to.
            json_payload: (Optional) Content of the request as JSON payload.
            data: (Optional) Content of the request.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """
        if data is None:
            content_type = 'application/json'
            if json_payload is None:
                payload = '{}' # The REST APIs don't support an empty payload
            else:
                payload = json.dumps(json_payload, indent=4)
        else:
            content_type = 'application/x-www-form-urlencoded'
            payload = data

        headers = {
            'Accept': 'application/json',
            'Content-Type': content_type,
        }

        return await self._send_request(
            method='POST',
            url=url,
            headers=headers,
            auth=BasicAuth(consumer_key, consumer_secret),
            data=payload,
        )

    async def requests_delete(
            self,
            access_token: str,
            url: str,
        ) -> None:
        r"""
        Sends a DELETE request.

        Args:
            access_token: The Access Token to use for authentication.
            url: Where to send the request to.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        return await self._send_request(
            method='DELETE',
            url=url,
            headers=headers,
        )

    async def requests_get(
            self,
            access_token: str,
            url: str,
            params: Dict[str, Any]=None,
        ) -> Any or None:
        r"""
        Sends a GET request.

        Args:
            access_token: The Access Token to use for authentication.
            url: Where to send the request to.
            params: (Optional) URL query parameters.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        return await self._send_request(
            method='GET',
            url=url,
            params=params,
            headers=headers,
        )

    async def requests_get_all(
            self,
            access_token: str,
            url: str,
            property_name: str,
            params: Dict[str, Any]=None,
            page_size: int=100,
        ) -> List[Any]:
        r"""
        Sends a GET request and returns all elements from all pages.

        Args:
            access_token: The Access Token to use for authentication.
            url: Where to send the request to.
            property_name: Name of the property that contains the elements of the page
            params: (Optional) URL query parameters.
            page_size: (Optional) number of elements per page.

        Returns:
            The list of elements from all pages.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """
        if params is None:
            params = {}

        elements: List[Any] = []

        while True:
            json_response = await self.requests_get(
                access_token=access_token,
                url=url,
                params=params,
            )

            if property_name in json_response:
                sub_result = json_response[property_name]
                for element in sub_result:
                    elements.append(element)

                if len(sub_result) < page_size:
                    break

            if not 'next' in json_response:
                break

            params['start'] = json_response['next']
            if params['start'] is None or params['start'] == '':
                break

        return elements

    async def requests_get_basic_auth(
            self,
            consumer_key: str,
            consumer_secret: str,
            url: str,
        ) -> Any or None:
        r"""
        Sends a GET request with Basic authentication.

        Args:
            consumer_key: The Dolby.io Consumer Key.
            consumer_secret: The Dolby.io Consumer Secret.
            url: Where to send the request to.

        Returns:
            The JSON response if any or None.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        return await self._send_request(
            method='GET',
            url=url,
            headers=headers,
            auth=BasicAuth(consumer_key, consumer_secret),
        )

    async def download(
            self,
            access_token: str,
            url: str,
            accept: str,
            file_path: str,
        ) -> None:
        r"""
        Downloads a file.

        Args:
            access_token: The Access Token to use for authentication.
            url: Where to send the request to.
            accept: Accept HTTP header.
            file_path: Where to save the file.

        Raises:
            HttpRequestError: If a client error one occurred.
            HTTPError: If one occurred.
        """
        headers = {
            'Accept': accept,
            'Authorization': f'Bearer {access_token}',
        }

        await self._download_file(
            url=url,
            headers=headers,
            file_path=file_path
        )

    async def _raise_for_status(self, http_response: ClientResponse):
        r"""Raises :class:`HttpRequestError` or :class:`ClientResponseError`, if one occurred."""

        if 400 <= http_response.status < 500:
            if self.log_verbose:
                if 400 < http_response.status < 404:
                    print(
                        f'{fg.red}[error]{fg.rs}',
                        f'Unauthorized to get data at the url {http_response.url} response code {http_response.status}'
                    )
                elif http_response.status == 404:
                    print(
                        f'{fg.red}[error]{fg.rs}',
                        f'Unable to get data from the url {http_response.url} Not found (404)'
                    )
                else:
                    print(
                        f'{fg.red}[error]{fg.rs}',
                        f'Did not find data at the url {http_response.url} response code {http_response.status}'
                    )

            try:
                json_response = await http_response.json()

                error_type = get_value_or_default(json_response, 'type', None)
                error_code = get_value_or_default(json_response, 'error_code', 0)
                if error_code == 0:
                    error_code = get_value_or_default(json_response, 'status', 0)
                error_reason = get_value_or_default(json_response, 'error_reason', None)
                if error_reason is None:
                    error_reason = get_value_or_default(json_response, 'error', None)
                error_description = get_value_or_default(json_response, 'error_description', None)
                if error_description is None:
                    error_description = get_value_or_default(json_response, 'message', None)

                raise HttpRequestError(http_response, error_type, error_code, error_reason, error_description)
            except (ValueError, ContentTypeError): # If the response body does not contain valid json.
                pass

        http_response.raise_for_status()
