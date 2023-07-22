from datetime import datetime


def parse_datetime(value):
    """
    Parse a timestamp string and return a datetime.

    Wrapper around datetime.fromisoformat for Python < 3.11.
    """
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        value = value.replace('Z', '+00:00')
        return datetime.fromisoformat(value)
