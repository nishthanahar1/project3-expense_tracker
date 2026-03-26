expenses = []

def add_expense(name, amount):
    expenses.append({'name': name, 'amount': amount})

def delete_expense(index):
    if 0 <= index < len(expenses):
        expenses.pop(index)

def calculate_total():
    return sum(int(e['amount']) for e in expenses)

# Add expenses
add_expense('Food', 100)
add_expense('Transport', 50)
add_expense('Books', 200)

print("Expenses:", expenses)
print("Total:", calculate_total())

# Delete one expense
delete_expense(1)

print("\nAfter delete:")
print("Expenses:", expenses)
print("Total:", calculate_total())
