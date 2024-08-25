This project demonstrates a simple Flask application with a login form vulnerable to SQL injection attacks. 

Key Features:

Flask application with a login form.
Vulnerable to SQL injection attacks.
Demonstrates the importance of parameterized queries and input validation

Running the Application:

Install dependencies: pip install Flask sqlite3
Run the application: python app.py
Exploring the Code:

The get_db function establishes a connection to the SQLite database.
The init_db function creates a users table and inserts sample data.
The / route displays the login form.
The /login route handles the login process and is vulnerable to SQL injection.
Mitigation:

Use parameterized queries to prevent SQL injection.
Sanitize user input before constructing SQL statements.
Note: This project is for educational purposes only. Always implement proper security measures in real-world applications.
