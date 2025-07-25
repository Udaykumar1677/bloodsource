from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# ✅ Reusable database connection
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'bloodsource.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Create necessary tables
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Donors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')

    # Blood Requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            location TEXT NOT NULL,
            reason TEXT NOT NULL
        )
    ''')

    # Blood Banks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_banks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            available_groups TEXT NOT NULL,
            units TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Call this once when app starts
create_tables()

# ✅ Home page
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Register Donor
@app.route('/register_donor', methods=['GET', 'POST'])
def register_donor():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        email = request.form['email']
        location = request.form['location']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO donors (name, blood_group, phone, email, location)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, blood_group, phone, email, location))
        conn.commit()
        conn.close()

        return redirect('/view_donors')
    return render_template('register_donor.html')

# View Donors
@app.route('/view_donors')
def view_donors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, blood_group, phone, email, location FROM donors")
    donors = cursor.fetchall()
    conn.close()
    return render_template('view_donors.html', donors=donors)


# ✅ Request Blood
@app.route('/request_blood', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        contact = request.form['contact']
        email = request.form['email']
        location = request.form['location']
        reason = request.form['reason']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO requests (name, blood_group, contact, email, location, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, blood_group, contact, email, location, reason))
        conn.commit()
        conn.close()

        return redirect('/view_requests')
    return render_template('request_blood.html')

# ✅ View Requests
@app.route('/view_requests')
def view_requests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    requests_data = cursor.fetchall()
    conn.close()
    return render_template('view_requests.html', requests=requests_data)

# ✅ Blood Banks - Add and View
@app.route('/blood_banks', methods=['GET', 'POST'])
def blood_banks():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        available_groups = request.form['available_groups']
        units = request.form['units']
        location = request.form['location']

        cursor.execute('''
            INSERT INTO blood_banks (name, available_groups, units, location)
            VALUES (?, ?, ?, ?)
        ''', (name, available_groups, units, location))
        conn.commit()

    cursor.execute("SELECT * FROM blood_banks")
    banks = cursor.fetchall()
    conn.close()

    return render_template('blood_banks.html', banks=banks)

# ✅ Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
