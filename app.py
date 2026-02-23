from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DB_FILE = 'library.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        available INTEGER DEFAULT 1
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        borrow_date TEXT,
        due_date TEXT,
        return_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )''')
    conn.commit()
    conn.close()

init_db()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()

# Books endpoints
@app.route('/api/books', methods=['GET'])
def get_books():
    books = query_db('SELECT * FROM books')
    return jsonify([dict(row) for row in books])

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    
    existing = query_db('SELECT * FROM books WHERE LOWER(title)=LOWER(?) AND LOWER(author)=LOWER(?)', (title, author))
    if existing:
        return jsonify({"message": "Book already exists in the system."}), 400
    
    execute_db('INSERT INTO books (title, author, available) VALUES (?, ?, 1)', (title, author))
    book = query_db('SELECT * FROM books WHERE title=? AND author=?', (title, author), one=True)
    return jsonify({"message": f"Book '{title}' added with ID {book['id']}."}), 201

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = query_db('SELECT * FROM books WHERE id=?', (book_id,), one=True)
    if not book:
        return jsonify({"message": "Book not found."}), 404
    if not book['available']:
        return jsonify({"message": "Cannot delete a borrowed book."}), 400
    execute_db('DELETE FROM books WHERE id=?', (book_id,))
    return jsonify({"message": f"Book '{book['title']}' deleted."})

@app.route('/api/books/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    results = query_db('SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?', (f'%{query.lower()}%', f'%{query.lower()}%'))
    return jsonify([dict(row) for row in results])

# Users endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    users = query_db('SELECT * FROM users')
    return jsonify([dict(row) for row in users])

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    existing = query_db('SELECT * FROM users WHERE LOWER(email)=LOWER(?)', (email,))
    if existing:
        return jsonify({"message": "Email already registered."}), 400
    
    execute_db('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    user = query_db('SELECT * FROM users WHERE email=?', (email,), one=True)
    return jsonify({"message": f"User '{name}' registered with ID {user['id']}."}), 201

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = query_db('SELECT * FROM users WHERE id=?', (user_id,), one=True)
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    active_loans = query_db('SELECT * FROM loans WHERE user_id=? AND return_date IS NULL', (user_id,))
    if active_loans:
        return jsonify({"message": "Cannot delete user with active loans."}), 400
    
    execute_db('DELETE FROM users WHERE id=?', (user_id,))
    return jsonify({"message": f"User '{user['name']}' deleted."})

# Loans endpoints
@app.route('/api/loans', methods=['GET'])
def get_loans():
    loans = query_db('SELECT * FROM loans')
    loan_data = []
    for loan in loans:
        book = query_db('SELECT * FROM books WHERE id=?', (loan['book_id'],), one=True)
        user = query_db('SELECT * FROM users WHERE id=?', (loan['user_id'],), one=True)
        status = "Returned" if loan['return_date'] else "Borrowed"
        due = datetime.strptime(loan['due_date'], "%Y-%m-%d").date()
        overdue = False
        if not loan['return_date']:
            if datetime.now().date() > due:
                overdue = True
        loan_data.append({
            "id": loan['id'],
            "user_name": user['name'] if user else "Unknown",
            "book_title": book['title'] if book else "Unknown",
            "borrow_date": loan['borrow_date'],
            "due_date": loan['due_date'],
            "return_date": loan['return_date'] or "-",
            "status": status,
            "overdue": overdue
        })
    return jsonify(loan_data)

@app.route('/api/loans', methods=['POST'])
def borrow_book():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    
    user = query_db('SELECT * FROM users WHERE id=?', (user_id,), one=True)
    book = query_db('SELECT * FROM books WHERE id=?', (book_id,), one=True)
    
    if not user or not book:
        return jsonify({"message": "Invalid user or book ID."}), 400
    if not book['available']:
        return jsonify({"message": "Book is not available."}), 400
    
    borrow_date = datetime.now().date()
    due_date = borrow_date + timedelta(days=14)
    execute_db('INSERT INTO loans (user_id, book_id, borrow_date, due_date, return_date) VALUES (?, ?, ?, ?, NULL)', 
               (user_id, book_id, str(borrow_date), str(due_date)))
    execute_db('UPDATE books SET available=0 WHERE id=?', (book_id,))
    return jsonify({"message": f"Book '{book['title']}' borrowed by {user['name']} (Due date: {due_date})."}), 201

@app.route('/api/loans/return', methods=['POST'])
def return_book():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    
    loan = query_db('SELECT * FROM loans WHERE user_id=? AND book_id=? AND return_date IS NULL', (user_id, book_id), one=True)
    if not loan:
        return jsonify({"message": "No active loan found for this user and book."}), 404
    
    execute_db('UPDATE loans SET return_date=? WHERE id=?', (str(datetime.now().date()), loan['id']))
    execute_db('UPDATE books SET available=1 WHERE id=?', (book_id,))
    book = query_db('SELECT * FROM books WHERE id=?', (book_id,), one=True)
    return jsonify({"message": f"Book '{book['title']}' returned successfully."})

# Serve static frontend
@app.route('/')
def serve_index():
    static_path = os.path.join(os.path.dirname(__file__), 'library_frontend', 'static')
    return send_from_directory(static_path, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    static_path = os.path.join(os.path.dirname(__file__), 'library_frontend', 'static')
    return send_from_directory(static_path, filename)

if __name__ == "__main__":
    print("=" * 50)
    print("Library Management System - Web Server")
    print("=" * 50)
    print("\nTo access from other devices on your network:")
    print("1. Find your computer's IP address:")
    print("   - Windows: Run 'ipconfig' in CMD")
    print("   - Look for IPv4 Address (e.g., 192.168.1.x)")
    print("\n2. On another device, open browser and go to:")
    print("   http://YOUR_IP_ADDRESS:5000/")
    print("\nServer running on http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
