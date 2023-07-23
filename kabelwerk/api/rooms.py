from kabelwerk.api.base import make_api_call
from kabelwerk.models import Message, Room, User
from kabelwerk.utils import parse_datetime


def update_room(*, hub='_', room, **kwargs):
    """
    Update a chat room.

    Return a named tuple with info about the updated room if the backend
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

    >>> # set the room's attributes to an empty dict
    >>> update_room(hub='section9', room='kusanagi', attributes={})
    Room(id=42, archived=False, attributes={}, hub_user=None)

    >>> # archive the room
    >>> update_room(hub='section9', room='kusanagi', archived=True)
    Room(id=42, archived=True, attributes={}, hub_user=None)

    >>> # unarchive the room
    >>> update_room(hub='section9', room='kusanagi', archived=False)
    Room(id=42, archived=False, attributes={}, hub_user=None)

    >>> # assign the room to a hub user
    >>> update_room(hub='section9', room='kusanagi', hub_user='batou')
    Room(id=42, archived=False, attributes={}, hub_user=User(key='batou'))

    >>> # unassign the room
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

    Return a named tuple with info about the newly created message if the
    backend accepts the request.

    Raise a ValidationError if the request is rejected because of invalid
    input.

    Raise an AuthenticationError if the request is rejected because the
    authentication token is invalid.

    Raise a ConnectionError if there is a problem connecting to the Kabelwerk
    backend or if the request times out.

    Raise a ServerError if the Kabelwerk backend fails to handle the request or
    behaves in an unexpected way.

    All arguments are named arguments.

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
