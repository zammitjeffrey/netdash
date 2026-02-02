import unittest
from app import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        # Create a test client for our Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        # Send a fake GET request to the home page
        response = self.app.get('/')
        # Assert that the server responds with 200 OK
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()