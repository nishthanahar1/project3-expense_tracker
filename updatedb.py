import sqlite3

conn = sqlite3.connect('expenses.db')
c = conn.cursor()

c.execute("ALTER TABLE expenses ADD COLUMN date TEXT")

conn.commit()
conn.close()

print("Date column added!")
