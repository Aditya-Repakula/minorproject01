import os
import sqlite3
import json
from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for, flash
from enhanced_chatbot import enhanced_rule_based_response

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-this-in-prod'
app.config['DATABASE'] = 'academic.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.open_resource('schema.sql', mode='r') as f:
        get_db().executescript(f.read())
    get_db().commit()

def seed_data():
    db = get_db()
    db.execute("INSERT OR IGNORE INTO users(username, password, role) VALUES ('admin', 'admin123', 'admin'), ('student', 'student123', 'student')")
    db.execute("INSERT OR IGNORE INTO faq(category, question, answer) VALUES ('rules', 'attendance rules', '75% attendance required')")
    db.execute("INSERT OR IGNORE INTO timetable(day, period, subject, room, faculty) VALUES ('Monday', 1, 'Math', 'A101', 'Prof. Sharma')")
    db.execute("INSERT OR IGNORE INTO exams(exam_name, date, subject, venue) VALUES ('Mid Sem', '2024-12-20', 'Math', 'Hall')")
    db.execute("INSERT OR IGNORE INTO contacts(department, faculty_name, email, phone) VALUES ('CS', 'Dr. Kumar', 'kumar@college.edu', '9876543210')")
    db.execute("INSERT OR IGNORE INTO assignments(course, title, due_date, description, submission_link) VALUES ('CS101', 'Assignment 1', '2024-12-25', 'Complete exercises', 'http://link.com')")
    db.execute("INSERT OR IGNORE INTO calendar(date, event) VALUES ('2024-12-25', 'Holiday')")
    db.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_db().execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect('/admin' if user['role'] == 'admin' else '/chat')
        return render_template('login_simple.html', error='Invalid credentials')
    return render_template('login_simple.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/chat')
def chat():
    if session.get('role') != 'student':
        return redirect('/')
    return render_template('chat.html')

@app.route('/chat/respond', methods=['POST'])
def chat_respond():
    if session.get('role') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    msg = request.get_json().get('message', '')
    return jsonify({'reply': enhanced_rule_based_response(msg, get_db())})

@app.route('/timetable')
def timetable():
    if session.get('role') != 'student':
        return redirect('/')
    entries = get_db().execute("SELECT * FROM timetable WHERE deleted_at IS NULL").fetchall()
    return render_template('timetable.html', entries=entries)

@app.route('/timetable/generate', methods=['POST'])
def timetable_generate():
    if session.get('role') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    subjects = ['Mathematics', 'Computer Science', 'Physics', 'Chemistry', 'English']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    plan = [{'day': days[i], 'subject': subjects[i % len(subjects)], 'duration': '2 hours', 'task': 'Review and Practice'} for i in range(len(days))]
    return jsonify({'plan': plan})

@app.route('/attendance')
def attendance():
    if session.get('role') != 'student':
        return redirect('/')
    return render_template('attendance.html')

@app.route('/attendance/calc', methods=['POST'])
def attendance_calc():
    data = request.get_json()
    a, t = int(data.get('attended', 0)), int(data.get('total', 1))
    percent = round((a / t) * 100, 2)
    needed = max(0, 3 * t - 4 * a)
    return jsonify({'percent': percent, 'classes_needed': needed})

@app.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('admin_enhanced.html')

@app.route('/admin/data/<kind>')
def admin_data(kind):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    rows = get_db().execute(f"SELECT * FROM {kind} WHERE deleted_at IS NULL").fetchall()
    return jsonify({'status': 'ok', 'data': [dict(r) for r in rows]})

@app.route('/admin/add/<kind>', methods=['POST'])
def admin_add(kind):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.form
    db = get_db()
    if kind == 'faq':
        db.execute("INSERT INTO faq (category, question, answer) VALUES (?, ?, ?)", (data['category'], data['question'], data['answer']))
    elif kind == 'timetable':
        db.execute("INSERT INTO timetable (day, period, subject, room, faculty) VALUES (?, ?, ?, ?, ?)", (data['day'], data['period'], data['subject'], data['room'], data['faculty']))
    elif kind == 'exams':
        db.execute("INSERT INTO exams (exam_name, date, subject, venue) VALUES (?, ?, ?, ?)", (data['exam_name'], data['date'], data['subject'], data['venue']))
    elif kind == 'contacts':
        db.execute("INSERT INTO contacts (department, faculty_name, email, phone) VALUES (?, ?, ?, ?)", (data['department'], data['faculty_name'], data['email'], data['phone']))
    elif kind == 'assignments':
        db.execute("INSERT INTO assignments (course, title, due_date, description, submission_link) VALUES (?, ?, ?, ?, ?)", (data['course'], data['title'], data['due_date'], data['description'], data['submission_link']))
    elif kind == 'calendar':
        db.execute("INSERT INTO calendar (date, event) VALUES (?, ?)", (data['date'], data['event']))
    db.commit()
    return jsonify({'status': 'ok', 'message': 'Added'})

@app.route('/admin/update/<kind>/<int:id>', methods=['POST'])
def admin_update(kind, id):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.form
    db = get_db()
    if kind == 'faq':
        db.execute("UPDATE faq SET category=?, question=?, answer=? WHERE id=?", (data['category'], data['question'], data['answer'], id))
    elif kind == 'timetable':
        db.execute("UPDATE timetable SET day=?, period=?, subject=?, room=?, faculty=? WHERE id=?", (data['day'], data['period'], data['subject'], data['room'], data['faculty'], id))
    elif kind == 'exams':
        db.execute("UPDATE exams SET exam_name=?, date=?, subject=?, venue=? WHERE id=?", (data['exam_name'], data['date'], data['subject'], data['venue'], id))
    elif kind == 'contacts':
        db.execute("UPDATE contacts SET department=?, faculty_name=?, email=?, phone=? WHERE id=?", (data['department'], data['faculty_name'], data['email'], data['phone'], id))
    elif kind == 'assignments':
        db.execute("UPDATE assignments SET course=?, title=?, due_date=?, description=?, submission_link=? WHERE id=?", (data['course'], data['title'], data['due_date'], data['description'], data['submission_link'], id))
    elif kind == 'calendar':
        db.execute("UPDATE calendar SET date=?, event=? WHERE id=?", (data['date'], data['event'], id))
    db.commit()
    return jsonify({'status': 'ok', 'message': 'Updated'})

@app.route('/admin/delete/<kind>/<int:id>', methods=['POST', 'DELETE'])
def admin_delete(kind, id):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    get_db().execute(f"UPDATE {kind} SET deleted_at = datetime('now') WHERE id = ?", (id,))
    get_db().commit()
    return jsonify({'status': 'ok', 'message': 'Deleted', 'item_name': f'{kind} #{id}'})

@app.route('/admin/bulk-delete', methods=['POST'])
def admin_bulk_delete():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    items = request.get_json().get('items', [])
    db = get_db()
    for item in items:
        db.execute(f"UPDATE {item['kind']} SET deleted_at = datetime('now') WHERE id = ?", (item['id'],))
    db.commit()
    return jsonify({'status': 'ok', 'deleted_count': len(items), 'total_requested': len(items), 'errors': []})

@app.route('/admin/audit-log')
def admin_audit_log():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'status': 'ok', 'logs': []})

if __name__ == '__main__':
    if not os.path.exists('academic.db'):
        with app.app_context():
            init_db()
            seed_data()
    app.run(debug=True, host='127.0.0.1', port=5000)
