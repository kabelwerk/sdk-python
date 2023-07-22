from datetime import datetime

from kabelwerk.api.base import make_api_call
from kabelwerk.models import Message, User


def post_message(*, hub, room, user, text):
    """
    Post a message in a chat room.

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
        inserted_at=datetime.fromisoformat(data['inserted_at']),
        room_id=data['room_id'],
        text=data['text'],
        type=data['type'],
        updated_at=datetime.fromisoformat(data['updated_at']),
        user=User(
            id=data['user']['id'],
            key=data['user']['key'],
            name=data['user']['name'],
        ),
    )
