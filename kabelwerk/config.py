import os
import re


"""
The URL of the Kabelwerk backend to connect to.
"""
KABELWERK_URL = os.getenv('KABELWERK_URL', 'hubdemo.kabelwerk.io')

"""
The API token to authenticate the requests to the Kabelwerk API with.
"""
KABELWERK_API_TOKEN = os.getenv('KABELWERK_API_TOKEN', '')


# the compiled regex used to parse KABELWERK_URL
_url_regex = re.compile(
    r'^(?P<scheme>(ws|http)s?:\/\/)?(?P<host>[0-9a-z.:-]+)\/?(?P<path>[a-z\/]+)?$',
    flags=re.IGNORECASE,
)


def _parse_url():
    """
    Parse KABELWERK_URL and return its scheme, host, and path.

    We use a regex instead of urllib.parse.urlparse or urllib3.util.parse_url
    because these are too permissive and do not do any validation.

    Helper for the get_*_url functions below.
    """
    match = _url_regex.match(KABELWERK_URL)

    if not match:
        raise ValueError(f'{KABELWERK_URL} is not a valid Kabelwerk URL.')

    return (
        match['scheme'].lower().strip(':/') if match['scheme'] else '',
        match['host'].lower(),
        match['path'].lower() if match['path'] else '',
    )


def get_socket_url():
    """
    Return the websocket URL.
    """
    raise NotImplementedError


def get_api_url():
    """
    Return the API URL.
    """
    scheme, host, _ = _parse_url()

    scheme = 'http' if scheme in ['http', 'ws'] else 'https'

    return f'{scheme}://{host}/api'


def get_api_token():
    """
    Return the KABELWERK_API_TOKEN token. Raise if it is not set yet.
    """
    if not KABELWERK_API_TOKEN:
        raise ValueError((
            'You need to set KABELWERK_API_TOKEN '
            'in order to make requests to the Kabelwerk API.'
        ))

    return KABELWERK_API_TOKEN
