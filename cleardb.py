import sqlite3

def clear_database():
    db = sqlite3.connect("booking.db", timeout=5)
    c = db.cursor()

    try:
        c.execute("""
            DELETE FROM bookings WHERE booking_id>3;
        """)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    clear_database()

#def init_db():
#    conn = sqlite3.connect("booking.db")
#    c = conn.cursor()
#    # Users table
#    c.execute("""
#    CREATE TABLE IF NOT EXISTS users(
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        username TEXT UNIQUE NOT NULL,
#        password TEXT NOT NULL
#    )
#    """)
#
#    # Ticket types table
#    c.execute("""
#    CREATE TABLE IF NOT EXISTS ticket_types(
#        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
#        type TEXT NOT NULL,
#        cost INTEGER NOT NULL
#    )
#    """)
#
#    # Bookings table
#    c.execute("""
#    CREATE TABLE IF NOT EXISTS bookings(
#        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
#        user_id INTEGER NOT NULL,
#        ticket_id INTEGER NOT NULL,
#        people INTEGER NOT NULL,
#        date TEXT NOT NULL,
#        FOREIGN KEY (user_id) REFERENCES users(id),
#        FOREIGN KEY (ticket_id) REFERENCES ticket_types(ticket_id)
#    )
#    """)
#    # hotelbooking table
#    c.execute("""
#    CREATE TABLE IF NOT EXISTS hotelbooking (
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        user_id INTEGER,
#        check_in TEXT,
#        check_out TEXT,
#        rooms INTEGER,
#        adults INTEGER,
#        children INTEGER
#    )
#    """)
#
#    conn.commit()
#    conn.close()