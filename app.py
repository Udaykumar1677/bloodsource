from flask import Flask, render_template, request, redirect, send_from_directory
import mysql.connector

app = Flask(__name__, static_url_path='', static_folder='static')

# ✅ Reusable DB connection
def get_db_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12787899",
        password="cMJDREvHib",
        database="sql12787899",
        port=3306
    )

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Register Donor
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
        cursor.execute("""
            INSERT INTO donors (name, blood_group, phone, email, location)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, blood_group, phone, email, location))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/view_donors')
    return render_template('register_donor.html')

# Request Blood
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
        cursor.execute("""
            INSERT INTO requests (name, blood_group, contact, email, location, reason)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, blood_group, contact, email, location, reason))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/view_requests')
    return render_template('request_blood.html')

# View Donors
@app.route('/view_donors')
def view_donors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, blood_group, phone, email, location FROM donors")
    donors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_donors.html', donors=donors)

# View Requests
@app.route('/view_requests')
def view_requests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    requests_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_requests.html', requests=requests_data)

# ✅ Serve sitemap
@app.route('/sitemap.xml')
def sitemap():
    return app.send_static_file('sitemap.xml')

# ✅ Serve robots.txt
@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')

# ✅ Google Site Verification File
@app.route('/google73e460509bc43d92.html')
def google_verify():
    return send_from_directory('.', 'google73e460509bc43d92.html')

# ✅ Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
