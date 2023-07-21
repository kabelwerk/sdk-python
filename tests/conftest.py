import logging

import pytest
import responses
from responses.matchers import header_matcher

from kabelwerk import config


@pytest.fixture
def api_url():
    # matches the default value of KABELWERK_URL
    return 'https://hubdemo.kabelwerk.io/api'


@pytest.fixture
def api_token():
    config.KABELWERK_API_TOKEN = 'TOKEN'
    yield 'TOKEN'
    config.KABELWERK_API_TOKEN = ''


@pytest.fixture
def mock_api():
    with responses.RequestsMock() as requests_mock:
        yield requests_mock


@pytest.fixture
def mock_response(api_url, api_token, mock_api):
    def function(method, url_path, status, payload=None):
        mock_api.add(
            method,
            api_url + url_path,
            match=[
                header_matcher({
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Kabelwerk-Token': api_token,
                }),
            ],
            status=status,
            json=payload,
        )

    return function


@pytest.fixture
def logs(caplog):
    caplog.set_level(logging.INFO)
    return caplog
