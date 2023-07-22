from datetime import datetime
from typing import NamedTuple


class User(NamedTuple):
    """
    A Kabelwerk user.
    """

    id: int
    """The user's unique integer ID in Kabelwerk's database."""

    key: str
    """Your unique ID for this user."""

    name: str
    """The user's name."""


class Room(NamedTuple):
    """
    A chat room.
    """

    id: int
    """The room's unique integer ID in Kabelwerk's database."""

    archived: bool
    """Whether the room is archived."""

    attributes: dict
    """The room's attributes."""

    hub_user: User | None
    """The hub user assigned to the room — if such."""

    user: User
    """The room's user."""


class Message(NamedTuple):
    """
    A chat message.
    """

    id: int
    """The message's unique integer ID in Kabelwerk's database."""

    html: str
    """The content of the message in HTML format."""

    inserted_at: datetime
    """Server-side timestamp of when the message was first stored in the database."""

    room_id: int
    """The ID of the room to which the message belongs."""

    text: str
    """The content of the message in plaintext format."""

    type: str
    """The type of the message."""

    updated_at: datetime
    """Server-side timestamp of when the message was last modified."""

    user: User
    """The user who posted the message."""
