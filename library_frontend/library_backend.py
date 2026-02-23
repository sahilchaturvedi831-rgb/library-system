import json
import os
from datetime import datetime, timedelta

# File paths
BOOKS_FILE = 'books.json'
USERS_FILE = 'users.json'
LOANS_FILE = 'loans.json'

# Helper function to load data from JSON files
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

# Helper function to save data to JSON files
def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Load initial data
books = load_data(BOOKS_FILE)
users = load_data(USERS_FILE)
loans = load_data(LOANS_FILE)

# Function to add a book (with duplicate check)
def add_book(title, author):
    if any(b for b in books if b["title"].lower() == title.lower() and b["author"].lower() == author.lower()):
        return {"success": False, "message": "Book already exists in the system."}
    book_id = max([b["id"] for b in books], default=0) + 1
    books.append({"id": book_id, "title": title, "author": author, "available": True})
    save_data(BOOKS_FILE, books)
    return {"success": True, "message": f"Book '{title}' added with ID {book_id}."}

# Function to delete a book
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return {"success": False, "message": "Book not found."}
    if not book["available"]:
        return {"success": False, "message": "Cannot delete a borrowed book."}
    books = [b for b in books if b["id"] != book_id]
    save_data(BOOKS_FILE, books)
    return {"success": True, "message": f"Book '{book['title']}' deleted."}

# Function to search books
def search_books(query):
    results = [b for b in books if query.lower() in b["title"].lower() or query.lower() in b["author"].lower()]
    if not results:
        return {"success": False, "message": "No books found matching the query.", "results": []}
    return {"success": True, "results": [{"id": b["id"], "title": b["title"], "author": b["author"], "available": b["available"]} for b in results]}

# Function to register a user (with duplicate email check)
def add_user(name, email):
    if any(u for u in users if u["email"].lower() == email.lower()):
        return {"success": False, "message": "Email already registered."}
    user_id = max([u["id"] for u in users], default=0) + 1
    users.append({"id": user_id, "name": name, "email": email})
    save_data(USERS_FILE, users)
    return {"success": True, "message": f"User '{name}' registered with ID {user_id}."}

# Function to borrow a book (with due date)
def borrow_book(user_id, book_id):
    user = next((u for u in users if u["id"] == user_id), None)
    book = next((b for b in books if b["id"] == book_id), None)
    if not user or not book:
        return {"success": False, "message": "Invalid user or book ID."}
    if not book["available"]:
        return {"success": False, "message": "Book is not available."}

    borrow_date = datetime.now().date()
    due_date = borrow_date + timedelta(days=14)
    loans.append({
        "user_id": user_id,
        "book_id": book_id,
        "borrow_date": str(borrow_date),
        "due_date": str(due_date),
        "return_date": None
    })
    book["available"] = False
    save_data(LOANS_FILE, loans)
    save_data(BOOKS_FILE, books)
    return {"success": True, "message": f"Book '{book['title']}' borrowed by {user['name']} (Due date: {due_date})."}

# Function to return a book
def return_book(user_id, book_id):
    loan = next((l for l in loans if l["user_id"] == user_id and l["book_id"] == book_id and l["return_date"] is None), None)
    if not loan:
        return {"success": False, "message": "No active loan found for this user and book."}
    loan["return_date"] = str(datetime.now().date())
    book = next(b for b in books if b["id"] == book_id)
    book["available"] = True
    save_data(LOANS_FILE, loans)
    save_data(BOOKS_FILE, books)
    return {"success": True, "message": f"Book '{book['title']}' returned successfully."}

# Function to view all books
def view_books():
    if not books:
        return {"success": False, "message": "No books in the system.", "books": []}
    return {"success": True, "books": [{"id": b["id"], "title": b["title"], "author": b["author"], "available": b["available"]} for b in books]}

# Function to view all users
def view_users():
    if not users:
        return {"success": False, "message": "No users registered.", "users": []}
    return {"success": True, "users": [{"id": u["id"], "name": u["name"], "email": u["email"]} for u in users]}

# View all loans
def view_loans():
    if not loans:
        return {"success": False, "message": "No loan records found.", "loans": []}
    loan_list = []
    for loan in loans:
        book = next((b for b in books if b["id"] == loan["book_id"]), {"title": "Unknown"})
        user = next((u for u in users if u["id"] == loan["user_id"]), {"name": "Unknown"})
        status = "Returned" if loan["return_date"] else "Borrowed"
        overdue = False
        if not loan["return_date"]:
            due = datetime.strptime(loan["due_date"], "%Y-%m-%d").date()
            if datetime.now().date() > due:
                overdue = True
        loan_list.append({
            "user": user["name"],
            "book": book["title"],
            "borrow_date": loan["borrow_date"],
            "due_date": loan["due_date"],
            "return_date": loan["return_date"],
            "status": status,
            "overdue": overdue
        })
    return {"success": True, "loans": loan_list}

# Export report to CSV (modified to return success message)
def export_report():
    import csv
    filename = f"library_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Book", "Borrowed", "Due", "Returned", "Status"])
        for loan in loans:
            user = next((u for u in users if u["id"] == loan["user_id"]), {"name": "Unknown"})
            book = next((b for b in books if b["id"] == loan["book_id"]), {"title": "Unknown"})
            status = "Returned" if loan["return_date"] else "Borrowed"
            writer.writerow([user["name"], book["title"], loan["borrow_date"], loan["due_date"], loan["return_date"] or "-", status])
    return {"success": True, "message": f"Report exported as '{filename}'."}
