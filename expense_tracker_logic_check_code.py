expenses = []

def add_expense(name, amount):
    expenses.append({'name': name, 'amount': amount})

def delete_expense(index):
    if 0 <= index < len(expenses):
        expenses.pop(index)

# Add items
add_expense('Food', 100)
add_expense('Transport', 50)
add_expense('Books', 200)

print("Before delete:", expenses)

# Delete the second expense
delete_expense(1)

print("After delete:", expenses)
