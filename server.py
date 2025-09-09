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
        if self.path == "/submit":
            length = int(self.headers.get("Content-Length"))
            body = self.rfile.read(length).decode()
            data = urllib.parse.parse_qs(body)
            name = data.get("username", ["Anonymous"])[0]

            html = f"""
            <!DOCTYPE html>
            <html>
              <head><link rel="stylesheet" href="styles.css"></head>
              <body>
                <h1>Hello, {name}!</h1>
                <a href="/">Go back</a>
              </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), MyHandler)
    print("Server running at http://0.0.0.0:8000")
    server.serve_forever()
