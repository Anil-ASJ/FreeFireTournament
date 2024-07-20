from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO registrations (name, email, phone)
            VALUES (?, ?, ?)
        ''', (name, email, phone))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/registrations')
def registrations():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registrations')
    registrations = cursor.fetchall()
    conn.close()
    
    return render_template('registrations.html', registrations=registrations)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
