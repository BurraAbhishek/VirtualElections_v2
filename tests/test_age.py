import datetime
import unittest
from math import floor


def calculateAge(target: list, reference: list) -> int:
    currentDate = datetime.datetime(
        year=reference[0],
        month=reference[1],
        day=reference[2]
    )
    birthDate = datetime.datetime(
        year=target[0],
        month=target[1],
        day=target[2]
    )
    age = (currentDate - birthDate).days
    return floor(age / 365.2425)


class TestAges(unittest.TestCase):

    def test_ages(self):
        self.assertEqual(
            first=calculateAge([2022, 1, 2], [2022, 1, 1]),
            second=-1
        )
        self.assertEqual(
            first=calculateAge([2016, 2, 29], [2022, 1, 1]),
            second=5
        )
