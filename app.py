from flask import Flask, request, g, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'test.db'

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close the database connection after the request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize the database (run once at start)
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
        cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'mypassword')")
        db.commit()

# Route for home page showing both forms
@app.route('/page')
def index():
    return render_template('index.html')

# Vulnerable Login (SQL Injection Possible)
@app.route('/vulnerable_login', methods=['POST'])
def vulnerable_login():
    username = request.form['username_vuln']
    password = request.form['password_vuln']
    db = get_db()
    cursor = db.cursor()
    
    # Vulnerable SQL query without parameterization
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        return "<h1>Vulnerable Login: Login successful!</h1>"
    else:
        return "<h1>Vulnerable Login: Invalid credentials!</h1>"

# Secure Login (Protected from SQL Injection)
@app.route('/secure_login', methods=['POST'])
def secure_login():
    username = request.form['username_secure']
    password = request.form['password_secure']
    db = get_db()
    cursor = db.cursor()

    # Secure SQL query with parameterization
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        return "<h1>Secure Login: Login successful!</h1>"
    else:
        return "<h1>Secure Login: Invalid credentials!</h1>"

# Initialize the database when the script runs
if __name__ == '__main__':
    init_db()  # Make sure the database is initialized
    app.run(debug=True)
