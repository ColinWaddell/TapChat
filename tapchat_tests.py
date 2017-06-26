import os
import tapchat
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_subtract_days(self):
        assert tapchat.subtract_days('Monday', 'Thursday') == 3
        assert tapchat.subtract_days('Saturday', 'Monday') == 2

if __name__ == '__main__':
    unittest.main()
