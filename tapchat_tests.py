import os
import tapchat
import unittest
import tempfile
import json

def get_sample_requests():
    with open('templates/sample_request.json') as sample_file:
        sample = json.load(sample_file)
    return json.loads(sample)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        tapchat.app.testing = True
        self.app = tapchat.app.test_client()

    def tearDown(self):
        pass

    def test_subtract_days(self):
        assert tapchat.subtract_days('Monday', 'Thursday') == 3
        assert tapchat.subtract_days('Saturday', 'Monday') == 2

if __name__ == '__main__':
    unittest.main()
