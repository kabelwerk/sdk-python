from datetime import datetime, timezone

from responses.matchers import json_params_matcher

from kabelwerk.api import post_message
from kabelwerk.models import Message, User


def test_post_message_works(mock_api, mock_response):
    """
    The post_message function should return a Message named tuple if the
    endpoint accepts the request.
    """
    mock_response('POST', '/hubs/section9/rooms/kusanagi/messages', 201, {
        'html': "<p>And where does the newborn go from here?</p>",
        'id': 16947,
        'inserted_at': '2023-07-22T09:46:57Z',
        'room_id': 22818,
        'text': "And where does the newborn go from here?",
        'type': 'text',
        'updated_at': '2023-07-22T09:46:57Z',
        'upload': None,
        'user': {
            'id': 49421,
            'key': 'batou',
            'name': 'Batou',
        },
    })

    message = post_message(
        hub='section9',
        room='kusanagi',
        user='batou',
        text='And where does the newborn go from here?'
    )

    assert len(mock_api.calls) == 1
    assert json_params_matcher({
        'text': 'And where does the newborn go from here?',
        'user': 'batou',
    })(mock_api.calls[0].request)

    assert isinstance(message, Message)
    assert message.html == "<p>And where does the newborn go from here?</p>"
    assert message.id == 16947
    assert message.inserted_at == datetime(2023, 7, 22, 9, 46, 57,
                                           tzinfo=timezone.utc)
    assert message.room_id == 22818
    assert message.text == "And where does the newborn go from here?"
    assert message.type == 'text'
    assert message.updated_at == datetime(2023, 7, 22, 9, 46, 57,
                                          tzinfo=timezone.utc)

    assert isinstance(message.user, User)
    assert message.user.id == 49421
    assert message.user.key == 'batou'
    assert message.user.name == 'Batou'
