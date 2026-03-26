from flask import Flask, render_template, request, redirect

app = Flask(__name__)

expenses = []

@app.route('/')
def index():
    total = sum(int(e['amount']) for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    amount = request.form['amount']
    expenses.append({'name': name, 'amount': amount})
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(expenses):
        expenses.pop(index)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
