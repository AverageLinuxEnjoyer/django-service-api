from random import randint, choice
from datetime import date, timedelta, datetime

def random_date(start: date, end: date) -> date:
    delta = end - start

    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_seconds = randint(0, int_delta)

    return start + timedelta(seconds=random_seconds)

def random_datetime(start: datetime, end: datetime) -> datetime:
    delta = end - start

    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_seconds = randint(0, int_delta)

    return start + timedelta(seconds=random_seconds)