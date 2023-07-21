from kabelwerk.api.base import make_api_call
from kabelwerk.models import User


def create_user(*, key, name, hub=None):
    """
    Create a user with the given key and name.

    Return a named tuple with info about the newly created user if the backend
    accepts the request.

    Raise a ValidationError if the request is rejected because of invalid
    input.

    Raise an AuthenticationError if the request is rejected because the
    authentication token is invalid.

    Raise a ConnectionError if there is a problem connecting to the Kabelwerk
    backend or if the request times out.

    Raise a ServerError if the Kabelwerk backend fails to handle the request or
    behaves in an unexpected way.

    All arguments are named arguments.

    >>> create_user(key='kusanagi', name='Motoko')
    User(id=42, key='kusanagi', name='Motoko')

    >>> create_user(name='Name Only')
    ValidationError

    """
    data = make_api_call('POST', '/users', {
        'hub': hub,
        'key': key,
        'name': name,
    })

    return User(
        id=data['id'],
        key=data['key'],
        name=data['name'],
    )


def update_user(*, key, name):
    """
    Update the user with the given key.

    Return a named tuple with info about the updated user if the backend
    accepts the request.

    Raise a ValidationError if the request is rejected because of invalid
    input.

    Raise an AuthenticationError if the request is rejected because the
    authentication token is invalid.

    Raise a ConnectionError if there is a problem connecting to the Kabelwerk
    backend or if the request times out.

    Raise a ServerError if the Kabelwerk backend fails to handle the request or
    behaves in an unexpected way.

    All arguments are named arguments.

    >>> update_user(key='kusanagi', name='Motoko')
    User(id=42, key='kusanagi', name='Motoko')

    >>> update_user(key='kusanagi', name='')
    ValidationError

    """
    data = make_api_call('PATCH', f'/users/{key}', {
        'name': name,
    })

    return User(
        id=data['id'],
        key=data['key'],
        name=data['name'],
    )


def delete_user(*, key):
    """
    Delete the user with the given key.

    Raise an AuthenticationError if the request is rejected because the
    authentication token is invalid.

    Raise a ConnectionError if there is a problem connecting to the Kabelwerk
    backend or if the request times out.

    Raise a ServerError if the Kabelwerk backend fails to handle the request or
    behaves in an unexpected way.

    All arguments are named arguments.

    >>> delete_user(key='kusanagi')
    None

    """
    make_api_call('DELETE', f'/users/{key}')
