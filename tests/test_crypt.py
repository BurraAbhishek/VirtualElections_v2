import unittest
from modules.common.crypt import str_decrypt, str_encrypt


class TestCrypt(unittest.TestCase):

    def test_crypt(self):
        self.assertEqual(
            first=str_decrypt(str_encrypt("Test")),
            second="Test"
        )
