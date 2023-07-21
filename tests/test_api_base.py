import logging

import pytest
from responses.matchers import json_params_matcher

from kabelwerk.api.base import make_api_call
from kabelwerk.exceptions import (
    AuthenticationError, ConnectionError, ServerError, ValidationError,
)


TEST_PARAMS = {'ghost': True}


def test_make_api_call_200(mock_api, mock_response, logs):
    """
    The make_api_call function should return the decoded response payload if
    the endpoint accepts the request.
    """
    mock_response('POST', '/test', 200, {'code': 2107})

    assert make_api_call('POST', '/test', TEST_PARAMS) == {'code': 2107}

    assert len(mock_api.calls) == 1
    assert json_params_matcher(TEST_PARAMS)(mock_api.calls[0].request)

    assert len(logs.records) == 1
    assert logs.records[0].levelno == logging.INFO
    assert logs.records[0].message == (
        "POST https://hubdemo.kabelwerk.io/api/test {'ghost': True} "
        "→ 200 OK {'code': 2107}"
    )


def test_make_api_call_400(mock_api, mock_response, logs):
    """
    The make_api_call function should raise if the endpoint rejects the request
    because its payload fails the validation.
    """
    mock_response('POST', '/test', 400, {'errors': {'field': ['message']}})

    with pytest.raises(ValidationError):
        make_api_call('POST', '/test', TEST_PARAMS)

    assert len(mock_api.calls) == 1
    assert json_params_matcher(TEST_PARAMS)(mock_api.calls[0].request)

    assert len(logs.records) == 1
    assert logs.records[0].levelno == logging.WARNING
    assert logs.records[0].message == (
        "POST https://hubdemo.kabelwerk.io/api/test {'ghost': True} "
        "→ 400 Bad Request {'errors': {'field': ['message']}}"
    )


def test_make_api_call_401(mock_api, mock_response, logs):
    """
    The make_api_call function should raise if the endpoint rejects the request
    because the Kabelwerk-Token is not valid.
    """
    mock_response('POST', '/test', 401, {})

    with pytest.raises(AuthenticationError):
        make_api_call('POST', '/test', TEST_PARAMS)

    assert len(mock_api.calls) == 1
    assert json_params_matcher(TEST_PARAMS)(mock_api.calls[0].request)

    assert len(logs.records) == 1
    assert logs.records[0].levelno == logging.ERROR
    assert logs.records[0].message == (
        "POST https://hubdemo.kabelwerk.io/api/test {'ghost': True} "
        "→ 401 Unauthorized"
    )


def test_make_api_call_500(mock_api, mock_response, logs):
    """
    The make_api_call function should raise if the backend fails to process the
    request because of a server error.
    """
    mock_response('POST', '/test', 500, {})

    with pytest.raises(ServerError):
        make_api_call('POST', '/test', TEST_PARAMS)

    assert len(mock_api.calls) == 1
    assert json_params_matcher(TEST_PARAMS)(mock_api.calls[0].request)

    assert len(logs.records) == 1
    assert logs.records[0].levelno == logging.ERROR
    assert logs.records[0].message == (
        "POST https://hubdemo.kabelwerk.io/api/test {'ghost': True} "
        "→ 500 Internal Server Error"
    )


def test_make_api_call_connection_error(api_token, mock_api, logs):
    """
    The make_api_call function should raise if there is an issue connecting to
    the backend.
    """
    with pytest.raises(ConnectionError):
        make_api_call('POST', '/test', TEST_PARAMS)

    assert len(mock_api.calls) == 1
    assert json_params_matcher(TEST_PARAMS)(mock_api.calls[0].request)

    assert len(logs.records) == 1
    assert logs.records[0].levelno == logging.ERROR
    assert logs.records[0].message.startswith((
        "POST https://hubdemo.kabelwerk.io/api/test {'ghost': True} "
        "→ Connection refused by Responses"
    ))
