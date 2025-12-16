from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "SECRET123"   # Change this in production

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/map")
def mappage():
    return render_template("map.html")

@app.route("/education")
def education():
    return render_template("education.html")
# Helper: get database connection
def get_db():
    # Make sure we get the DB name by checking the config for a DATABASE or assigning it a default one
    db = app.config.get("DATABASE", "booking.db") 
    return sqlite3.connect(db, check_same_thread=False)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        c = db.cursor()
        # Insert new user
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            db.close()  
        except:
            return "User already exists"
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        c = db.cursor()
        c.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        db.close()  
        if user:
            session["user_id"] = user[0]
            session["username"] = username
            return redirect("/")
        else:
            return "Invalid login"
    return render_template("login.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    # must be logged in
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        user_id = session.get('user_id', 1)
        booking_date = request.form["date"]
        adults = int(request.form['adults'])
        children = int(request.form['children'])
        students = int(request.form['students'])
        ticket_type=request.form["ticket-type"]

        db = get_db()
        c = db.cursor()

        try:
            c.execute('INSERT INTO bookings (user_id, booking_date, adults, children, students, ticket_type) VALUES (?, ?, ?, ?, ?, ?)',
                      (user_id, booking_date, adults, children, students, ticket_type))
            db.commit() 
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            c.close()
            db.close()  
        return redirect(url_for('my_bookings'))

    return render_template("booking.html")


@app.route("/hotel", methods=["GET", "POST"])
def hotel():
    
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        user_id = session["user_id"]
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]
        guests = int(request.form["guests"])
        room_type = request.form["room_type"]

        conn = sqlite3.connect("booking.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("""
            INSERT INTO hotel_bookings (user_id, check_in, check_out, guests, room_type)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, check_in, check_out, guests, room_type))
        conn.commit()
        conn.close()
        return redirect(url_for("my_bookings"))

    return render_template("hotel_booking.html")

def init_db():
   conn = get_db()
   c = conn.cursor()
   # Users table
   c.execute("""
   CREATE TABLE IF NOT EXISTS users(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL
   )
   """)

   # Ticket types table
   c.execute("""
   CREATE TABLE IF NOT EXISTS ticket_types(
       ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
       type TEXT NOT NULL,
       cost INTEGER NOT NULL
   )
   """)

   # Bookings table
   c.execute("""
   CREATE TABLE IF NOT EXISTS bookings(
       booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
       FOREIGN KEY (user_id) REFERENCES users(id),
       booking_date DATE NOT NULL,
       adults INTEGER DEFAULT 1 NOT NULL,
       childred INTEGER DEFAULT 0,
       students INTEGER DEFAULT 0,
        ticekt_type TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   )
   """)
   # hotelbooking table
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

   conn.commit()
   conn.close()

@app.route("/my-bookings")
def my_bookings():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = sqlite3.connect("booking.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT booking_date, adults, children, students, ticket_type, created_at FROM bookings WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    zoo_bookings = c.fetchall()

    c.execute("SELECT check_in, check_out, guests, room_type, created_at FROM hotel_bookings WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    hotel_bookings = c.fetchall()

    conn.close()
    return render_template("my_bookings.html", zoo_bookings=zoo_bookings, hotel_bookings=hotel_bookings)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))