import logging

import requests

from kabelwerk.config import get_api_token, get_api_url
from kabelwerk.exceptions import (
    AuthenticationError, ConnectionError, ServerError, ValidationError,
)


logger = logging.getLogger('kabelwerk.api')


def make_api_call(method, url_path, params=None, timeout=2):
    """
    Send a request to the Kabelwerk API.

    Return the response payload if the request is accepted. Return None if the
    response is accepted but does not have payload.

    Raise a ValidationError if the request is rejected because of invalid
    input.

    Raise an AuthenticationError if the request is rejected because the
    authentication token is invalid.

    Raise a ConnectionError if there is a problem connecting to the Kabelwerk
    backend or if the request times out.

    Raise a ServerError if the Kabelwerk backend fails to handle the request or
    behaves in an unexpected way.

    In all cases, write a log entry.
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

    else:
        logger.error(f'{log} → {response.status_code} {response.reason}')

        raise ServerError(response)
