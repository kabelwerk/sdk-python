from responses.matchers import json_params_matcher

from kabelwerk.api import create_user, delete_user


def test_create_user_works(mock_api, mock_response):
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

    assert len(mock_api.calls) == 1
    assert json_params_matcher({
        'hub': None,
        'key': 'kusanagi',
        'name': 'Motoko',
    })(mock_api.calls[0].request)

    assert user.id == 2
    assert user.key == 'kusanagi'
    assert user.name == 'Motoko'


def test_delete_user_works(mock_api, mock_response):
    """
    The delete_user function should return None if the endpoint accepts the
    request.
    """
    mock_response('DELETE', '/users/kusanagi', 204)

    output = delete_user(key='kusanagi')

    assert len(mock_api.calls) == 1
    assert mock_api.calls[0].request.body is None

    assert output is None
