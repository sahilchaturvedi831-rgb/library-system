from flask import Flask, request, jsonify
from library_backend import (
    add_book, delete_book, search_books, add_user, borrow_book, return_book,
    view_books, view_users, view_loans, export_report
)

app = Flask(__name__)

@app.route('/add_book', methods=['POST'])
def api_add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    if not title or not author:
        return jsonify({"success": False, "message": "Title and author are required."}), 400
    result = add_book(title, author)
    return jsonify(result)

@app.route('/delete_book', methods=['POST'])
def api_delete_book():
    data = request.json
    try:
        book_id = int(data.get('book_id'))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid book ID."}), 400
    result = delete_book(book_id)
    return jsonify(result)

@app.route('/search_books', methods=['GET'])
def api_search_books():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"success": False, "message": "Query is required."}), 400
    result = search_books(query)
    return jsonify(result)

@app.route('/add_user', methods=['POST'])
def api_add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({"success": False, "message": "Name and email are required."}), 400
    result = add_user(name, email)
    return jsonify(result)

@app.route('/borrow_book', methods=['POST'])
def api_borrow_book():
    data = request.json
    try:
        user_id = int(data.get('user_id'))
        book_id = int(data.get('book_id'))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid user or book ID."}), 400
    result = borrow_book(user_id, book_id)
    return jsonify(result)

@app.route('/return_book', methods=['POST'])
def api_return_book():
    data = request.json
    try:
        user_id = int(data.get('user_id'))
        book_id = int(data.get('book_id'))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid user or book ID."}), 400
    result = return_book(user_id, book_id)
    return jsonify(result)

@app.route('/view_books', methods=['GET'])
def api_view_books():
    result = view_books()
    return jsonify(result)

@app.route('/view_users', methods=['GET'])
def api_view_users():
    result = view_users()
    return jsonify(result)

@app.route('/view_loans', methods=['GET'])
def api_view_loans():
    result = view_loans()
    return jsonify(result)

@app.route('/export_report', methods=['POST'])
def api_export_report():
    result = export_report()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
