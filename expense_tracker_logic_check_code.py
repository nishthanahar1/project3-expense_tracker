import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, name TEXT, amount INTEGER)''')
    conn.commit()
    conn.close()

def add_expense(name, amount):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (name, amount) VALUES (?, ?)', (name, amount))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    data = c.fetchall()
    conn.close()
    return data

def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id=?', (id,))
    conn.commit()
    conn.close()

def calculate_total():
    expenses = get_expenses()
    return sum(e[2] for e in expenses)

# Initialize DB
init_db()

# Add expenses
add_expense('Food', 100)
add_expense('Transport', 50)
add_expense('Books', 200)

print("Before delete:", get_expenses())
print("Total:", calculate_total())

# Delete expense with id = 2
delete_expense(2)

print("\nAfter delete:", get_expenses())
print("Total:", calculate_total())
