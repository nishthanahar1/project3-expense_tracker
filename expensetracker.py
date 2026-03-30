from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  amount INTEGER,
                  category TEXT,
                  date TEXT,
                  note TEXT)''')
    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses ORDER BY date DESC')
    data = c.fetchall()
    conn.close()
    return data


def add_expense(name, amount, category, date, note):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (name, amount, category, date, note) VALUES (?, ?, ?, ?, ?)',
              (name, amount, category, date, note))
    conn.commit()
    conn.close()


def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id=?', (id,))
    conn.commit()
    conn.close()


def update_expense(id, name, amount, category, note):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('UPDATE expenses SET name=?, amount=?, category=?, note=? WHERE id=?',
              (name, amount, category, note, id))
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
    category = request.form['category']
    date = request.form['date']
    note = request.form['note']

    add_expense(name, amount, category, date, note)
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    delete_expense(id)
    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        category = request.form['category']
        note = request.form['note']

        update_expense(id, name, amount, category, note)
        return redirect('/')

    c.execute('SELECT * FROM expenses WHERE id=?', (id,))
    expense = c.fetchone()
    conn.close()

    return render_template('edit.html', expense=expense)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
