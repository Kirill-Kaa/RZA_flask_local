import unittest
from app import app, init_db, get_db  # import your Flask instance
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
        self.assertEqual(response.status_code, 200)#

    def test_education(self):
       response = self.client.get("/education")
       self.assertEqual(response.status_code, 200)
       #this tests if the text exists in your page so we know it loaded
       self.assertIn(b"Engaging real-life learning experiences", response.data)


    def test_user_saved_in_database(self):
        self.client.post("/register", data={"username": "Bob", "password": "123456"}, follow_redirects=True)
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = 'Bob'")
        result = c.fetchone()
        print(result)
        conn.close()
        self.assertIsNotNone(result)
    
    def test_booking_saved_in_database(self):
        # Register a user first
        self.client.post("/register", data={"username": "Alice", "password": "abcdef"}, follow_redirects=True)
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE username = 'Alice'")
        user_id = c.fetchone()[0]

        # Insert a booking for that user
        c.execute("""
            INSERT INTO hotel_bookings (user_id, check_in, check_out, room_type)
            VALUES (?, ?, ?, ?)
        """, (user_id, "2025-12-10", "2025-12-12", "Deluxe"))
        conn.commit()

        # Verify booking exists
        c.execute("SELECT user_id, check_in, check_out, guests, room_type FROM hotel_bookings WHERE user_id=?", (user_id,))
        booking = c.fetchone()
        conn.close()

        self.assertIsNotNone(booking, "Booking should be inserted")
        self.assertEqual(booking[0], user_id)
        self.assertEqual(booking[1], "2025-12-10")
        self.assertEqual(booking[2], "2025-12-12")
        self.assertEqual(booking[3], 1)  # default guests
        self.assertEqual(booking[4], "Deluxe")
        

    def tearDown(self):
        if os.path.exists("test.db"):
                os.remove("test.db")

    
if __name__ == "__main__":
    unittest.main()
