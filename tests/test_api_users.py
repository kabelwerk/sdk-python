import pytest
from responses.matchers import json_params_matcher

from kabelwerk.api import create_user
from kabelwerk.exceptions import (
    AuthenticationError, ServerError, ValidationError,
)


def test_create_user_201(mock_api, mock_response):
    """
    The create_user function should return a User named tuple if the endpoint
    accepts the request.
    """
    mock_response('POST', '/users', 201, {
        'id': 2,
        'key': 'kusanagi',
        'name': 'Motoko',
    })

    user = create_user(name='Motoko', key='kusanagi')
    assert user.id == 2
    assert user.key == 'kusanagi'
    assert user.name == 'Motoko'

    assert len(mock_api.calls) == 1
    assert json_params_matcher({
        'hub': None,
        'key': 'kusanagi',
        'name': 'Motoko',
    })(mock_api.calls[0].request)


def test_create_user_400(mock_api, mock_response):
    """
    The create_user function should raise if the endpoint rejects the request
    because its payload fails the validation.
    """
    mock_response('POST', '/users', 400, {})

    with pytest.raises(ValidationError):
        create_user(name='Motoko', key='kusanagi')

    assert len(mock_api.calls) == 1


def test_create_user_401(mock_api, mock_response):
    """
    The create_user function should raise if the endpoint rejects the request
    because the Kabelwerk-Token is not valid.
    """
    mock_response('POST', '/users', 401, {})

    with pytest.raises(AuthenticationError):
        create_user(name='Motoko', key='kusanagi')

    assert len(mock_api.calls) == 1


def test_create_user_500(mock_api, mock_response):
    """
    The create_user function should raise if the backend fails to process the
    request because of an internal error.
    """
    mock_response('POST', '/users', 500, {})

    with pytest.raises(ServerError):
        create_user(name='Motoko', key='kusanagi')

    assert len(mock_api.calls) == 1
