from kabelwerk.api.base import make_api_call
from kabelwerk.models import Message, Room, User
from kabelwerk.utils import parse_datetime


def update_room(*, hub='_', room, **kwargs):
    """
    Update a chat room.

    All arguments are named arguments.


    Arguments
    ---------

    hub
        The slug identifying the hub to which the room belongs. You can omit
        this argument if you only have one hub.

    room
        Your unique ID of the end user to which the room belongs.

    archived
        Whether to mark the room as archived. Optional.

    attributes
        The attributes to set on the room. Optional.

    hub_user
        Your unique ID of the hub user to assign the room to. Set to None if
        you want to unassign the room. Optional.


    Returns
    -------

    typing.NamedTuple
        Info about the updated room if the backend accepts the request.


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

    Set the room's attributes to an empty dict:

    >>> update_room(hub='section9', room='kusanagi', attributes={})
    Room(id=42, archived=False, attributes={}, hub_user=None)


    Archive the room:

    >>> update_room(hub='section9', room='kusanagi', archived=True)
    Room(id=42, archived=True, attributes={}, hub_user=None)


    Unarchive the room:

    >>> update_room(hub='section9', room='kusanagi', archived=False)
    Room(id=42, archived=False, attributes={}, hub_user=None)


    Assign the room to a hub user:

    >>> update_room(hub='section9', room='kusanagi', hub_user='batou')
    Room(id=42, archived=False, attributes={}, hub_user=User(key='batou'))


    Unassign the room:

    >>> update_room(hub='section9', room='kusanagi', hub_user=None)
    Room(id=42, archived=False, attributes={}, hub_user=None)

    """
    params = {
        key: value for key, value in kwargs.items()
        if key in ['archived', 'attributes', 'hub_user']
    }

    data = make_api_call('PATCH', f'/hubs/{hub}/rooms/{room}', params)

    return Room(
        archived=data['archived'],
        attributes=data['attributes'],
        hub_user=User(
            id=data['hub_user']['id'],
            key=data['hub_user']['key'],
            name=data['hub_user']['name'],
        ) if data['hub_user'] else None,
        id=data['id'],
        user=User(
            id=data['user']['id'],
            key=data['user']['key'],
            name=data['user']['name'],
        ),
    )


"""
messages
"""


def post_message(*, hub='_', room, user, text):
    """
    Post a message in a chat room.

    All arguments are named arguments.


    Arguments
    ---------

    hub
        The slug identifying the hub to which the belongs the room where to
        post the message. You can omit this argument if you only have one hub.

    room
        Your unique ID of the end user to which belongs the room where to post
        the message.

    text
        The text of the message.


    Returns
    -------

    typing.NamedTuple
        Info about the newly posted message if the backend accepts the request.


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

    >>> post_message(hub='section9', room='kusanagi', user='batou', text='?')
    Message(id=42, key='kusanagi', name='Motoko')

    >>> post_message(hub='section9', room='kusanagi', user='batou', text='')
    ValidationError

    """
    data = make_api_call('POST', f'/hubs/{hub}/rooms/{room}/messages', {
        'text': text,
        'user': user,
    })

    return Message(
        html=data['html'],
        id=data['id'],
        inserted_at=parse_datetime(data['inserted_at']),
        room_id=data['room_id'],
        text=data['text'],
        type=data['type'],
        updated_at=parse_datetime(data['updated_at']),
        user=User(
            id=data['user']['id'],
            key=data['user']['key'],
            name=data['user']['name'],
        ),
    )
