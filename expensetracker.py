from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, name TEXT, amount INTEGER)''')
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    data = c.fetchall()
    conn.close()
    return data

def add_expense(name, amount):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (name, amount) VALUES (?, ?)', (name, amount))
    conn.commit()
    conn.close()

def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id=?', (id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    expenses = get_expenses()
    total = sum(e[2] for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    amount = request.form['amount']
    add_expense(name, amount)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    delete_expense(id)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
