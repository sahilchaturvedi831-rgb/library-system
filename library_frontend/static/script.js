const API_BASE = `${window.location.protocol}//${window.location.host}/api`;

// Helper function to display messages
function displayMessage(elementId, message, isSuccess) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="message ${isSuccess ? 'success' : 'error'}">${message}</div>`;
    setTimeout(() => element.innerHTML = '', 5000);
}

// Add Book
document.getElementById('add-book-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('book-title').value;
    const author = document.getElementById('book-author').value;
    const response = await fetch(`${API_BASE}/books`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, author })
    });
    const result = await response.json();
    displayMessage('add-book-message', result.message, response.ok);
    if (response.ok) e.target.reset();
});

// Delete Book
document.getElementById('delete-book-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const book_id = document.getElementById('delete-book-id').value;
    const response = await fetch(`${API_BASE}/books/${parseInt(book_id)}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
    });
    const result = await response.json();
    displayMessage('delete-book-message', result.message, response.ok);
    if (response.ok) e.target.reset();
});

// Search Books
document.getElementById('search-books-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('search-query').value;
    const response = await fetch(`${API_BASE}/books/search?q=${encodeURIComponent(query)}`);
    const result = await response.json();
    const resultsDiv = document.getElementById('search-results');
    let html = '<table><tr><th>ID</th><th>Title</th><th>Author</th><th>Status</th></tr>';
    result.forEach(book => {
        html += `<tr><td>${book.id}</td><td>${book.title}</td><td>${book.author}</td><td>${book.available ? 'Available' : 'Borrowed'}</td></tr>`;
    });
    html += '</table>';
    resultsDiv.innerHTML = html;
});

// Add User
document.getElementById('add-user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('user-name').value;
    const email = document.getElementById('user-email').value;
    const response = await fetch(`${API_BASE}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email })
    });
    const result = await response.json();
    displayMessage('add-user-message', result.message, response.ok);
    if (response.ok) e.target.reset();
});

// Borrow Book
document.getElementById('borrow-book-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const user_id = document.getElementById('borrow-user-id').value;
    const book_id = document.getElementById('borrow-book-id').value;
    const response = await fetch(`${API_BASE}/loans`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: parseInt(user_id), book_id: parseInt(book_id) })
    });
    const result = await response.json();
    displayMessage('borrow-book-message', result.message, response.ok);
    if (response.ok) e.target.reset();
});

// Return Book
document.getElementById('return-book-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const user_id = document.getElementById('return-user-id').value;
    const book_id = document.getElementById('return-book-id').value;
    const response = await fetch(`${API_BASE}/loans/return`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: parseInt(user_id), book_id: parseInt(book_id) })
    });
    const result = await response.json();
    displayMessage('return-book-message', result.message, response.ok);
    if (response.ok) e.target.reset();
});

// View Books
document.getElementById('view-books-btn').addEventListener('click', async () => {
    const response = await fetch(`${API_BASE}/books`);
    const result = await response.json();
    const listDiv = document.getElementById('books-list');
    let html = '<table><tr><th>ID</th><th>Title</th><th>Author</th><th>Status</th></tr>';
    result.forEach(book => {
        html += `<tr><td>${book.id}</td><td>${book.title}</td><td>${book.author}</td><td>${book.available ? 'Available' : 'Borrowed'}</td></tr>`;
    });
    html += '</table>';
    listDiv.innerHTML = html;
});

// View Users
document.getElementById('view-users-btn').addEventListener('click', async () => {
    const response = await fetch(`${API_BASE}/users`);
    const result = await response.json();
    const listDiv = document.getElementById('users-list');
    let html = '<table><tr><th>ID</th><th>Name</th><th>Email</th></tr>';
    result.forEach(user => {
        html += `<tr><td>${user.id}</td><td>${user.name}</td><td>${user.email}</td></tr>`;
    });
    html += '</table>';
    listDiv.innerHTML = html;
});

// View Loans
document.getElementById('view-loans-btn').addEventListener('click', async () => {
    const response = await fetch(`${API_BASE}/loans`);
    const result = await response.json();
    const listDiv = document.getElementById('loans-list');
    let html = '<table><tr><th>User</th><th>Book</th><th>Borrowed</th><th>Due</th><th>Returned</th><th>Status</th><th>Overdue</th></tr>';
    result.forEach(loan => {
        const overdueClass = loan.overdue ? ' style="color: red;"' : '';
        html += `<tr><td>${loan.user_name}</td><td>${loan.book_title}</td><td>${loan.borrow_date}</td><td>${loan.due_date}</td><td>${loan.return_date}</td><td>${loan.status}</td><td${overdueClass}>${loan.overdue ? 'OVERDUE' : ''}</td></tr>`;
    });
    html += '</table>';
    listDiv.innerHTML = html;
});
