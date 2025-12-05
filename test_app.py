import unittest
from app import app, init_db  # import your Flask instance
import os
class TestPageLoad(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config["SECRET_KEY"] = "test"
        app.config["DATABASE"] = "test.db"
     # 2. Delete old DB BEFORE anything opens it
        if os.path.exists("test.db"):
            os.remove("test.db")

        # 3. Now build fresh schema
        init_db()

        # 4. Create test client
        self.client = app.test_client()

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
