from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Change if you have a password set
    database="bloodsource"
)
cursor = db.cursor()

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

        cursor.execute("""
            INSERT INTO donors (name, blood_group, phone, email, location)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, blood_group, phone, email, location))
        db.commit()
        return redirect('/view_donors')
    return render_template('register_donor.html')

# Request Blood
@app.route('/request_blood', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        email = request.form['email']
        location = request.form['location']
        reason = request.form['reason']

        cursor.execute("""
            INSERT INTO requests (name, blood_group, phone, email, location, reason)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, blood_group, phone, email, location, reason))
        db.commit()
        return redirect('/view_requests')
    return render_template('request_blood.html')

# View Donors
@app.route('/view_donors')
def view_donors():
    cursor.execute("SELECT name, blood_group, phone, email, location FROM donors")
    donors = cursor.fetchall()
    return render_template('view_donors.html', donors=donors)

# View Requests
@app.route('/view_requests')
def view_requests():
    cursor.execute("SELECT * FROM requests")
    requests_data = cursor.fetchall()
    return render_template('view_requests.html', requests=requests_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
