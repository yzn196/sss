from flask import Flask, render_template, request, jsonify
from checker_and_crack_time import check_password_strength, estimate_crack_time
from generate_strong_password import generate_strong_password
import sqlite3

app = Flask(__name__)

# دالة إنشاء قاعدة البيانات والجدول تلقائياً عند تشغيل السيرفر
def init_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL,
            length INTEGER NOT NULL,
            strength TEXT NOT NULL,
            crack_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# تنفيذ دالة الإنشاء فوراً
init_db()

# دالة مساعدة لحفظ السجلات في قاعدة البيانات
def save_to_history(password, strength, crack_time):
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO history (password, length, strength, crack_time)
            VALUES (?, ?, ?, ?)
        ''', (password, len(password), strength, crack_time))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database error:", e)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.get_json() or {}
    password = data.get('password', '')

    if not password:
        return jsonify({'error': 'No password provided'}), 400

    strength = check_password_strength(password)
    crack_time = estimate_crack_time(password)

    # حفظ عملية الفحص في السجل
    save_to_history(password, strength, crack_time)

    return jsonify({
        'strength': strength,
        'crack_time': crack_time
    })


@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json() or {}
    length = data.get('length', 16)

    if not (8 <= length <= 50):
        length = 16

    generated_pass = generate_strong_password(length)
    strength = check_password_strength(generated_pass)
    crack_time = estimate_crack_time(generated_pass)

    # حفظ كلمة السر المولدة في السجل
    save_to_history(generated_pass, strength, crack_time)

    return jsonify({'password': generated_pass})


@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password, length, strength, crack_time, created_at FROM history ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()

        history_list = []
        for row in rows:
            history_list.append({
                'id': row[0],
                'password': row[1],
                'length': row[2],
                'strength': row[3],
                'crack_time': row[4],
                'created_at': row[5]
            })

        return jsonify(history_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


    