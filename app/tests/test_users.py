from app import application
import unittest

class UsersTests(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = application.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_get_user(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/user/1')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)