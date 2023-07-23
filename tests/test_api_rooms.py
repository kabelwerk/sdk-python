from datetime import datetime, timezone

from responses.matchers import json_params_matcher

from kabelwerk.api import post_message, update_room
from kabelwerk.models import Message, Room, User


def test_update_room_attributes(mock_api, mock_response):
    """
    One should be able to set the custom attributes of a room in an explicitly
    specified hub.
    """
    mock_response('PATCH', '/hubs/section9/rooms/kusanagi', 200, {
        'archived': False,
        'attributes': {
            'seven': 7,
        },
        'hub_user': {
            'id': 49448,
            'key': 'batou',
            'name': 'Batou',
        },
        'id': 22833,
        'user': {
            'id': 49447,
            'key': 'kusanagi',
            'name': 'Motoko',
        },
    })

    room = update_room(
        hub='section9',
        room='kusanagi',
        attributes={'seven': 7},
    )

    assert len(mock_api.calls) == 1
    assert json_params_matcher({
        'attributes': {'seven': 7},
    })(mock_api.calls[0].request)

    assert isinstance(room, Room)
    assert room.archived is False
    assert room.attributes == {'seven': 7}
    assert room.id == 22833

    assert isinstance(room.hub_user, User)
    assert room.hub_user.id == 49448
    assert room.hub_user.key == 'batou'
    assert room.hub_user.name == 'Batou'

    assert isinstance(room.user, User)
    assert room.user.id == 49447
    assert room.user.key == 'kusanagi'
    assert room.user.name == 'Motoko'


def test_update_room_no_hub_archived(mock_api, mock_response):
    """
    One should be able to archive a room in the default hub.
    """
    mock_response('PATCH', '/hubs/_/rooms/kusanagi', 200, {
        'archived': True,
        'attributes': {},
        'hub_user': None,
        'id': 22833,
        'user': {
            'id': 49447,
            'key': 'kusanagi',
            'name': 'Motoko',
        },
    })

    room = update_room(room='kusanagi', archived=True)

    assert len(mock_api.calls) == 1
    assert json_params_matcher({
        'archived': True,
    })(mock_api.calls[0].request)

    assert isinstance(room, Room)
    assert room.archived is True
    assert room.attributes == {}
    assert room.hub_user is None
    assert room.id == 22833

    assert isinstance(room.user, User)
    assert room.user.id == 49447
    assert room.user.key == 'kusanagi'
    assert room.user.name == 'Motoko'


"""
messages
"""


def test_post_message_text(mock_api, mock_response):
    """
    One should be able to post a text message in a room in an explicitly
    specified hub.
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


def test_post_message_no_hub_text(mock_api, mock_response):
    """
    One should be able to post a text message in a room in the default hub.
    """
    mock_response('POST', '/hubs/_/rooms/kusanagi/messages', 201, {
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
