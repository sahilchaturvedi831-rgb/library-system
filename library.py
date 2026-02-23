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
        return "Book already exists in the system."
    book_id = max([b["id"] for b in books], default=0) + 1
    books.append({"id": book_id, "title": title, "author": author, "available": True})
    save_data(BOOKS_FILE, books)
    return f"Book '{title}' added with ID {book_id}."

# Function to delete a book
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return "Book not found."
    if not book["available"]:
        return "Cannot delete a borrowed book."
    books = [b for b in books if b["id"] != book_id]
    save_data(BOOKS_FILE, books)
    return f"Book '{book['title']}' deleted."

# Function to search books
def search_books(query):
    results = [b for b in books if query.lower() in b["title"].lower() or query.lower() in b["author"].lower()]
    if not results:
        return []
    return results

# Function to register a user (with duplicate email check)
def add_user(name, email):
    if any(u for u in users if u["email"].lower() == email.lower()):
        return "Email already registered."
    user_id = max([u["id"] for u in users], default=0) + 1
    users.append({"id": user_id, "name": name, "email": email})
    save_data(USERS_FILE, users)
    return f"User '{name}' registered with ID {user_id}."

# Function to delete a user
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return "User not found."
    # Check for active loans
    active_loans = [l for l in loans if l["user_id"] == user_id and l["return_date"] is None]
    if active_loans:
        return "Cannot delete user with active loans."
    users = [u for u in users if u["id"] != user_id]
    save_data(USERS_FILE, users)
    return f"User '{user['name']}' deleted."

# Function to borrow a book (with due date)
def borrow_book(user_id, book_id):
    user = next((u for u in users if u["id"] == user_id), None)
    book = next((b for b in books if b["id"] == book_id), None)
    if not user or not book:
        return "Invalid user or book ID."
    if not book["available"]:
        return "Book is not available."
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
    return f"Book '{book['title']}' borrowed by {user['name']} (Due date: {due_date})."

# Function to return a book
def return_book(user_id, book_id):
    loan = next((l for l in loans if l["user_id"] == user_id and l["book_id"] == book_id and l["return_date"] is None), None)
    if not loan:
        return "No active loan found for this user and book."
    loan["return_date"] = str(datetime.now().date())
    book = next(b for b in books if b["id"] == book_id)
    book["available"] = True
    save_data(LOANS_FILE, loans)
    save_data(BOOKS_FILE, books)
    return f"Book '{book['title']}' returned successfully."

# Function to view all books
def view_books():
    if not books:
        return []
    return books

# Function to view all users
def view_users():
    if not users:
        return []
    return users

# View all loans
def view_loans():
    if not loans:
        return []
    loan_data = []
    for loan in loans:
        book = next((b for b in books if b["id"] == loan["book_id"]), {"title": "Unknown"})
        user = next((u for u in users if u["id"] == loan["user_id"]), {"name": "Unknown"})
        status = "Returned" if loan["return_date"] else "Borrowed"
        due = datetime.strptime(loan["due_date"], "%Y-%m-%d").date()
        overdue = False
        if not loan["return_date"]:
            if datetime.now().date() > due:
                overdue = True
        loan_data.append({
            "user_name": user["name"],
            "book_title": book["title"],
            "borrow_date": loan["borrow_date"],
            "due_date": loan["due_date"],
            "return_date": loan["return_date"] or "-",
            "status": status,
            "overdue": overdue
        })
    return loan_data

# Export report to CSV
def export_report():
    filename = f"library_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["User", "Book", "Borrowed", "Due", "Returned", "Status"])
        for loan in loans:
            user = next((u for u in users if u["id"] == loan["user_id"]), {"name": "Unknown"})
            book = next((b for b in books if b["id"] == loan["book_id"]), {"title": "Unknown"})
            status = "Returned" if loan["return_date"] else "Borrowed"
            writer.writerow([user["name"], book["title"], loan["borrow_date"], loan["due_date"], loan["return_date"] or "-", status])
    return f"Report exported as '{filename}'."

# Main CLI interface
if __name__ == "__main__":
    import csv
    
    while True:
        print("\n=== Library Management System ===")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Books")
        print("4. Add User")
        print("5. View Users")
        print("6. Borrow Book")
        print("7. Return Book")
        print("8. View Loans")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            print(add_book(title, author))
        elif choice == "2":
            print(view_books())
        elif choice == "3":
            query = input("Enter search query: ")
            print(search_books(query))
        elif choice == "4":
            name = input("Enter user name: ")
            email = input("Enter email: ")
            print(add_user(name, email))
        elif choice == "5":
            print(view_users())
        elif choice == "6":
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            print(borrow_book(user_id, book_id))
        elif choice == "7":
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            print(return_book(user_id, book_id))
        elif choice == "8":
            print(view_loans())
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")
