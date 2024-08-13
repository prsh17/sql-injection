from flask import Flask, request, g
import sqlite3

app = Flask(__name__)
DATABASE = 'test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
        cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'mypassword')")
        db.commit()

@app.route('/')
def index():
    return '''
         <html>
    <head>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f2f2f2;
                margin: 0;
                font-family: Arial, sans-serif;
            }
            .login-container {
                background: #fff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border-radius: 8px;
                text-align: center;
            }
            .login-container h1 {
                margin-bottom: 20px;
            }
            .form-group {
                margin-bottom: 15px;
                text-align: left;
            }
            .form-group label {
                display: inline-block;
                width: 100px;
                text-align: right;
            }
            .form-group input {
                padding: 10px;
                width: calc(100% - 120px);
                margin-left: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .login-container input[type="submit"] {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .login-container input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>Login</h1>
            <form action="/login" method="post">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username">
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password">
                </div>
                <input type="submit" value="Login">
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    if user:
        return "Login successful!"
    else:
        return "Invalid credentials!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
