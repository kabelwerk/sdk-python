from kabelwerk.api.base import make_api_call
from kabelwerk.models import User


def create_user(*, key, name, hub=None):
    """
    Create a user with the given key and name.

    All arguments are named arguments.


    Arguments
    ---------

    key
        Your unique ID for this user.

    name
        The user's name.

    hub
        The slug identifying the hub in which to create the user. Only set this
        if you want to create a hub user.


    Returns
    -------

    typing.NamedTuple
        Info about the newly created user if the backend accepts the request.


    Raises
    ------

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


    Examples
    --------

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

    All arguments are named arguments.


    Arguments
    ---------

    key
        Your unique ID for this user.

    name
        The user's name.


    Returns
    -------

    typing.NamedTuple
        Info about the updated user if the backend accepts the request.


    Raises
    ------

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


    Examples
    --------

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

    All arguments are named arguments.


    Arguments
    ---------

    key
        Your unique ID for this user.

    Returns
    -------

    None


    Raises
    ------

    AuthenticationError
        If the request is rejected because the authentication token is invalid.

    ConnectionError
        If there is a problem connecting to the Kabelwerk backend or if the
        request times out.

    ServerError
        If the Kabelwerk backend fails to handle the request or behaves in an
        unexpected way.


    Examples
    --------

    >>> delete_user(key='kusanagi')
    None

    """
    make_api_call('DELETE', f'/users/{key}')
