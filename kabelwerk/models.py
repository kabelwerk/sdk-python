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
