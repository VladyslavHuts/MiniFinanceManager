from datetime import datetime


class Transaction:
    def __init__(self, amount, category, transaction_type, date=None):
        if transaction_type not in ["income", "expense"]:
            raise ValueError("Transaction type must be either 'income' or 'expense'")
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return f"{self.date} - {self.transaction_type.capitalize()}: {self.category} - {self.amount} UAH"

    def to_file_string(self):
        return f"{self.amount},{self.category},{self.transaction_type},{self.date}"

    @staticmethod
    def from_file_string(line):
        amount, category, transaction_type, date = line.strip().split(',')
        return Transaction(float(amount), category, transaction_type, date)


class FinanceManager:
    def __init__(self, file_name="transactions.txt"):
        self.file_name = file_name

    def add_transaction(self, transaction):
        """Додає транзакцію до файлу."""
        with open(self.file_name, "a") as file:
            file.write(transaction.to_file_string() + "\n")

    def view_transactions(self):
        """Зчитує всі транзакції з файлу та повертає список об'єктів Transaction."""
        transactions = []
        with open(self.file_name, "r") as file:
            for line in file:
                transaction = Transaction.from_file_string(line)
                transactions.append(transaction)
        return transactions

    def delete_transaction(self, date, category):
        """Видаляє транзакцію за датою та категорією."""
        transactions = self.view_transactions()
        transactions = [t for t in transactions if not (t.date == date and t.category == category)]

        with open(self.file_name, "w") as file:
            for transaction in transactions:
                file.write(transaction.to_file_string() + "\n")

    def calculate_balance(self):
        """Розраховує баланс на основі доходів і витрат."""
        income, expense = 0, 0
        transactions = self.view_transactions()
        for transaction in transactions:
            if transaction.transaction_type == "income":
                income += transaction.amount
            elif transaction.transaction_type == "expense":
                expense += transaction.amount
        return income - expense
