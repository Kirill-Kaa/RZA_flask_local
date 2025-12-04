import unittest
from app import app  # import your Flask instance

class TestPageLoad(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_register_page_loads(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)   # optional

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)      # optional

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
