from datetime import datetime, timezone

def now():
    """Returns the current datetime in utc without time zone info"""
    return datetime.now(timezone.utc).replace(tzinfo=None)