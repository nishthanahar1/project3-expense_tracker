from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv

app = Flask(__name__)

BUDGET = 5000

# ---------------- DATABASE ---------------- #

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


def search_expenses(query):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE name LIKE ?", ('%' + query + '%',))
    data = c.fetchall()
    conn.close()
    return data


# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    expenses = get_expenses()

    total = sum(e[2] for e in expenses)

    # Weekly
    week_ago = datetime.now() - timedelta(days=7)
    weekly = sum(e[2] for e in expenses if datetime.strptime(e[4], "%Y-%m-%d") >= week_ago)

    # Monthly
    month_ago = datetime.now() - timedelta(days=30)
    monthly = sum(e[2] for e in expenses if datetime.strptime(e[4], "%Y-%m-%d") >= month_ago)

    # Insights
    data = {}
    for e in expenses:
        data[e[3]] = data.get(e[3], 0) + e[2]

    top_category = max(data, key=data.get) if data else "None"

    warning = total > BUDGET

    return render_template('index.html',
                           expenses=expenses,
                           total=total,
                           weekly=weekly,
                           monthly=monthly,
                           top=top_category,
                           warning=warning)


@app.route('/add', methods=['POST'])
def add():
    add_expense(
        request.form['name'],
        request.form['amount'],
        request.form['category'],
        request.form['date'],
        request.form['note']
    )
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
        update_expense(
            id,
            request.form['name'],
            request.form['amount'],
            request.form['category'],
            request.form['note']
        )
        return redirect('/')

    c.execute('SELECT * FROM expenses WHERE id=?', (id,))
    expense = c.fetchone()
    conn.close()

    return render_template('edit.html', expense=expense)


@app.route('/search')
def search():
    query = request.args.get('q')
    expenses = search_expenses(query)

    total = sum(e[2] for e in expenses)

    return render_template('index.html',
                           expenses=expenses,
                           total=total,
                           weekly=0,
                           monthly=0,
                           top="Filtered",
                           warning=False)


# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
def dashboard():
    expenses = get_expenses()

    data = {}
    for e in expenses:
        data[e[3]] = data.get(e[3], 0) + e[2]

    if data:
        # Pie
        plt.figure()
        plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
        plt.title("Spending by Category")
        plt.savefig('static/pie.png')

        # Bar
        plt.figure()
        plt.bar(data.keys(), data.values())
        plt.title("Category Spending")
        plt.savefig('static/bar.png')

    return render_template('dashboard.html')


# ---------------- EXPORT ---------------- #

@app.route('/export')
def export():
    expenses = get_expenses()

    with open('expenses.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Amount', 'Category', 'Date', 'Note'])

        for e in expenses:
            writer.writerow([e[1], e[2], e[3], e[4], e[5]])

    return "CSV Exported!"

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
