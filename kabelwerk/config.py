import re


"""
The URL of the Kabelwerk backend to connect to.
"""
KABELWERK_URL = 'hubdemo.kabelwerk.io'

"""
The API token to authenticate the requests to the Kabelwerk API with.
"""
KABELWERK_API_TOKEN = ''


def _parse_url():
    """
    Parse KABELWERK_URL and return its scheme, host, and path.

    Helper for the get_*_url functions below.
    """
    match = re.match(
        r'^(?P<scheme>(ws|http)s?:\/\/)?(?P<host>[0-9a-z.:-]+)\/?(?P<path>[a-z\/]+)?$',
        KABELWERK_URL,
        flags=re.IGNORECASE,
    )

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
