import unittest
from mfcc import *


class HelpersTestCase(unittest.TestCase):

    def test_mfcc(self):
        mfcc = Mfcc()
        self.assertTrue(mfcc.encode("\01\01\02\02\03\03") == ["!", "!"])
        self.assertTrue(mfcc.encode("\01\01\02\02\03\03") == ["!", "!", "!"])
        return

if __name__ == '__main__':
    unittest.main()
