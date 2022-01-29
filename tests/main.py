import unittest
import sys
sys.path.append("../")
from tests import test_shrug
from tests import test_crypt
from tests import test_age


def create_testsuite():
    ldr = unittest.TestLoader()
    ts = unittest.TestSuite()
    ts.addTest(test=ldr.loadTestsFromModule(test_shrug))
    ts.addTest(test=ldr.loadTestsFromModule(test_crypt))
    ts.addTest(test=ldr.loadTestsFromModule(test_age))
    return ts


if __name__ == "__main__":
    s = create_testsuite()
    r = unittest.TextTestRunner()
    r.run(s)