"""
import sqlite3

with sqlite3.connect("users.db") as conn:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);")

with sqlite3.connect("app.db") as conn:
    conn.row_factory = sqlite3.Row
    user_number = input("Enter user number to fetch: ")
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_number)).fetchone()
    print(dict(user))
    """
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import mimetypes
import sqlite3

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):               
        # Default to index.html
        path = self.path.lstrip("/")
        if path == "":
            path = "index.html"

        if os.path.isfile(path):
            # Guess MIME type (e.g. text/html, text/css)
            mime, _ = mimetypes.guess_type(path)
            if not mime:
                mime = "application/octet-stream"

            with open(path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-type", mime)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(body)

        # Extract form fields
        username = data.get("username", [""])[0]
        password = data.get("password", [""])[0]
        password_again = data.get("password_again", [""])[0]

        if self.path == "/signup":
            success, msg = handle_signup(username, password, password_again)
            if success:
                self.send_response(302)  # redirect
                self.send_header("Location", "/login.html")
                self.end_headers()
            else:
                self.respond_with_message(msg)

        elif self.path == "/login":
            success, msg = handle_login(username, password)
            if success:
                self.respond_with_message(msg)
            else:
                self.respond_with_message(msg, status=401)
    
    def respond_with_message(self, message, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(message.encode())

def handle_signup(username, password, password_again):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    if password != password_again:
        return False, "Passwords do not match"

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "Signup successful"
    except sqlite3.IntegrityError:
        return False, "Username already taken"
    finally:
        conn.close()

def handle_login(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return True, f"Welcome back, {username}!"
    else:
        return False, "Invalid username or password"


    
        
if __name__ == "__main__":
    with sqlite3.connect("users.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL           
        )
        """)
    server = HTTPServer(("127.0.0.1", 8000), MyHandler)
    print("Server running at http://127.0.0.1:8000")
    server.serve_forever()
