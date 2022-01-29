import unittest
from modules.common.shrug import is_shrug
from modules.common.voteridgen import gen_id


class TestShrug(unittest.TestCase):

    def test_shrug(self):
        self.assertTrue(is_shrug("00000000"))
        self.assertTrue(is_shrug("Abcd1234"))
        self.assertTrue(is_shrug("A1b2C3de45f6G7H8"))
        self.assertTrue(is_shrug("ab12c3D4"))
        self.assertTrue(is_shrug("ABCDEFGH"))
        self.assertTrue(is_shrug("abcdefgh"))
        self.assertTrue(is_shrug("123456789"))
        self.assertTrue(is_shrug(gen_id(8)))
        self.assertTrue(is_shrug(gen_id(12)))
        self.assertFalse(is_shrug("{'$where': {'_id': '1' $or '1 == 1'}}"))
        self.assertFalse(is_shrug("sleep(10000)"))
        self.assertFalse(is_shrug("%d%d"))

