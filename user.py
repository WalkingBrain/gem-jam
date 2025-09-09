import sqlite3
with sqlite3.connect("app.db") as conn:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);")
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?);", (name, age))
