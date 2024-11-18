import unittest
from finance_manager import FinanceManager, Transaction
import os


class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        self.manager = FinanceManager("transactions.txt")
        with open("transactions.txt", "w") as file:
            file.truncate(0)

    def test_add_transaction(self):
        transaction = Transaction(amount=100, category="Food", transaction_type="expense")
        self.manager.add_transaction(transaction)
        with open("transactions.txt", "r") as file:
            content = file.read()
        self.assertIn("100,Food,expense", content)

    def test_clear_transactions(self):
        with open("transactions.txt", "w") as file:
            file.truncate(0)

    def test_calculate_balance(self):
        income = Transaction(amount=200, category="Salary", transaction_type="income")
        expense = Transaction(amount=50, category="Food", transaction_type="expense")

        self.manager.add_transaction(income)
        self.manager.add_transaction(expense)

        balance = self.manager.calculate_balance()
        print(f"Calculated balance: {balance}")
        self.assertEqual(balance, 150)


if __name__ == "__main__":
    unittest.main()
