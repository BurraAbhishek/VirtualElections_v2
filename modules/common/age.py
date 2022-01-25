import datetime
from math import floor


def calculateAge(year: int, month: int, day: int) -> int:
    currentDate = datetime.datetime.now()
    birthDate = datetime.datetime(year=year, month=month, day=day)
    age = (currentDate - birthDate).days
    return floor(age / 365.2425)
