import logging

import requests

from kabelwerk import __version__
from kabelwerk.config import get_api_token, get_api_url
from kabelwerk.exceptions import (
    AuthenticationError, ConnectionError, DoesNotExist, ServerError,
    ValidationError,
)


logger = logging.getLogger('kabelwerk.api')


def make_api_call(method, url_path, params=None, timeout=2):
    """
    Send a request to the Kabelwerk API.

    In all cases, write a log entry.


    Arguments
    ---------

    method
        The HTTP method.

    url_path
        The URL path of the endpoint.

    params
        The payload — if such — to encode and send with the request.

    timeout
        The number of seconds to wait for a response before giving up and
        raising a ConnectionError.


    Returns
    -------

    dict
        The decoded response payload if the request is accepted.

    None
        If the response is accepted but does not have payload.


    Raises
    ------

    DoesNotExist
        If the request is rejected because the requested entity does not exist.

    ValidationError
        If the request is rejected because of invalid input.

    AuthenticationError
        If the request is rejected because the authentication token is invalid.

    ConnectionError
        If there is a problem connecting to the Kabelwerk backend or if the
        request times out.

    ServerError
        If the Kabelwerk backend fails to handle the request or behaves in an
        unexpected way.

    """
    url = get_api_url() + url_path

    log = f'{method} {url}'
    if params:
        log = f'{log} {params!r}'

    try:
        response = requests.request(
            method,
            url,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Kabelwerk-Token': get_api_token(),
                'User-Agent': f'sdk-python/{__version__}',
            },
            json=params,
            timeout=timeout,
        )

    except requests.RequestException as error:
        logger.error(f'{log} → {error!s}', exc_info=error)

        raise ConnectionError(error)

    if response.status_code in [200, 201]:
        payload = response.json()

        logger.info((
            f'{log} → {response.status_code} {response.reason} {payload!r}'
        ))

        return payload

    elif response.status_code == 204:
        logger.info(f'{log} → {response.status_code} {response.reason}')

        return

    elif response.status_code == 400:
        payload = response.json()

        logger.warning((
            f'{log} → {response.status_code} {response.reason} {payload!r}'
        ))

        try:
            field = sorted(payload['errors'].keys())[0]
            error_message = payload['errors'][field][0]
        except (IndexError, KeyError):
            raise ServerError(response)

        raise ValidationError(response, field, error_message)

    elif response.status_code in [401, 403]:
        logger.error(f'{log} → {response.status_code} {response.reason}')

        raise AuthenticationError(response)

    elif response.status_code == 404:
        logger.warning(f'{log} → {response.status_code} {response.reason}')

        raise DoesNotExist(response)

    else:
        logger.error(f'{log} → {response.status_code} {response.reason}')

        raise ServerError(response)
