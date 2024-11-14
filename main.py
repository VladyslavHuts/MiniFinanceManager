from flask import Flask, render_template, request, redirect, url_for, flash
from finance_manager.finance_manager import Transaction, FinanceManager

app = Flask(__name__)
app.secret_key = '35cv56363xv7'  # Задайте випадковий секретний ключ для Flask

# Ініціалізуємо FinanceManager
manager = FinanceManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    try:
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        transaction_type = request.form.get("transaction_type")

        if transaction_type not in ["income", "expense"]:
            flash("Неправильний тип транзакції. Спробуйте ще раз.")
            return redirect(url_for("index"))

        transaction = Transaction(amount, category, transaction_type)
        manager.add_transaction(transaction)
        flash("Транзакцію додано!")
    except ValueError:
        flash("Введіть правильну суму.")
    return redirect(url_for("index"))

@app.route("/view_transactions")
def view_transactions():
    transactions = manager.view_transactions()
    return render_template("view_transactions.html", transactions=transactions)

@app.route("/calculate_balance")
def calculate_balance():
    balance = manager.calculate_balance()
    return render_template("balance.html", balance=balance)

if __name__ == "__main__":
    app.run(debug=True)
