from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os
import google.generativeai as genai  # ✅ Gemini AI integration

app = Flask(__name__)

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyCdIAKn4sl9OBeVSkKvcZoRNVhONQUTwk0")  # 🔑 Replace with your valid Gemini API key

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

# ✅ View Donors
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

# ✅ Blood Banks
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

# ✅ Update Blood Bank
@app.route('/update_bank/<int:id>', methods=['POST'])
def update_bank(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE blood_banks 
        SET name = ?, available_groups = ?, units = ?, location = ?
        WHERE id = ?
    ''', (data['name'], data['available_groups'], data['units'], data['location'], id))
    conn.commit()
    conn.close()
    return ('', 204)

# ✅ Delete Blood Bank
@app.route('/delete_bank/<int:id>')
def delete_bank(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blood_banks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/blood_banks')

# ✅ AI Chatbox (Enhanced with Telugu Support & Neat Output)
chat_sessions = {}

@app.route('/ai_chat', methods=['GET', 'POST'])
def ai_chat():
    user_input = None
    ai_response = None

    if 'chat' not in chat_sessions:
        model = genai.GenerativeModel("gemini-2.0-flash")
        chat_sessions['chat'] = model.start_chat()

    chat = chat_sessions['chat']

    if 'history' not in chat_sessions:
        chat_sessions['history'] = []

    history = chat_sessions['history']

    if request.method == 'POST':
        user_input = request.form.get('question')

        # --- Detect Telugu Request ---
        is_telugu = "telugu" in user_input.lower() or "తెలుగు" in user_input

        # --- Prepare prompt ---
        prompt = f"""
You are BloodSource AI Assistant.
The user might ask for blood banks in any Indian city.
Fetch and list *all* available blood banks in that city with:
- Hospital/Blood Bank Name 🏥
- Address 📍
- Contact Number ☎️ (if known)
- Available Blood Groups 🩸
- Units Available

Make the answer neat and professional using bullet points and emojis.

If the user asks "in Telugu" or uses Telugu words, translate your final answer into Telugu.

User query: {user_input}
"""

        try:
            response = chat.send_message(prompt)
            ai_response = response.text.strip()
        except Exception as e:
            ai_response = f"⚠️ Error: {str(e)}"

        # Save chat
        history.append({
            "id": len(history) + 1,
            "question": user_input,
            "answer": ai_response
        })

    return render_template(
        "ai_chatbox.html",
        user_input=user_input,
        ai_response=ai_response,
        history=history
    )
    
# ✅ Delete a specific chat message by ID
@app.route('/delete_chat/<int:qa_id>', methods=['POST'])
def delete_chat(qa_id):
    # Check if chat history exists
    if 'history' in chat_sessions and len(chat_sessions['history']) > 0:
        chat_sessions['history'] = [
            msg for msg in chat_sessions['history'] if msg['id'] != qa_id
        ]
    return redirect('/ai_chat')

# ✅ Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
