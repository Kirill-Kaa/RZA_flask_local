import sqlite3

def clear_database():
    db = sqlite3.connect("booking.db", timeout=5)
    c = db.cursor()

    try:
        c.execute("DROP TABLE hotelbooking")
        c.execute("""
            
            
        CREATE TABLE hotel_bookings (
            hotel_booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            guests INTEGER DEFAULT 1,
            room_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );


            """)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    clear_database()