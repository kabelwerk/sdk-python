import pytest

from kabelwerk import config


def test_bad_urls():
    """
    The get_api_url function should raise if KABELWERK_URL is not a valid URL.
    """
    for bad_url in ['', 'not a url']:
        config.KABELWERK_URL = bad_url

        with pytest.raises(ValueError):
            config.get_api_url()


def test_good_urls():
    """
    The get_api_url function should infer the API URL from KABELWERK_URL.
    """
    config.KABELWERK_URL = 'kabelwerk.io'
    assert config.get_api_url() == 'https://kabelwerk.io/api'

    config.KABELWERK_URL = 'hub.kabelwerk.io'
    assert config.get_api_url() == 'https://hub.kabelwerk.io/api'

    config.KABELWERK_URL = 'http://kabelwerk.io/api'
    assert config.get_api_url() == 'http://kabelwerk.io/api'

    config.KABELWERK_URL = 'https://kabelwerk.io/'
    assert config.get_api_url() == 'https://kabelwerk.io/api'

    config.KABELWERK_URL = 'WS://KABELWERK.IO'
    assert config.get_api_url() == 'http://kabelwerk.io/api'

    config.KABELWERK_URL = 'wss://kabelwerk.io/socket/hub'
    assert config.get_api_url() == 'https://kabelwerk.io/api'


def test_get_api_token():
    """
    The get_api_token function should raise if KABELWERK_API_TOKEN is not set.
    """
    with pytest.raises(ValueError):
        config.get_api_token()

    config.KABELWERK_API_TOKEN = 'TOKEN'
    assert config.get_api_token() == 'TOKEN'
