import sqlite3

conn = sqlite3.connect('expenses.db')
c = conn.cursor()

c.execute("SELECT * FROM expenses")
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()
