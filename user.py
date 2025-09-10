import sqlite3
with sqlite3.connect("users.db") as conn:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    users = conn.execute("SELECT * FROM users;").fetchall()
    for user in users:
        print(dict(user))
