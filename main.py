from flask import Flask, render_template, request, redirect, url_for, flash
from finance_manager.finance_manager import Transaction, FinanceManager

app = Flask(__name__)
app.secret_key = '35cv56363xv7'

manager = FinanceManager()

@app.route("/")
def index():
    try:
        with open("transactions.txt", "r") as file:
            balance = float(file.readline().strip())
    except FileNotFoundError:
        balance = 0.0
    except ValueError:
        balance = 0.0

    # Передаємо баланс у шаблон
    return render_template("index.html", balance=balance)


@app.route("/recharge")
def recharge():
    return render_template("recharge.html")

@app.route("/remove")
def remove():
    return render_template("remove.html")

@app.route("/transaction")
def transaction():
    return render_template("transaction.html")

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    try:
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        transaction_type = request.form.get("transaction_type")
        date = request.form.get("date")

        if transaction_type not in ["income", "expense"]:
            flash("Неправильний тип транзакції. Спробуйте ще раз.")
            return redirect(url_for("transaction"))

        with open("transactions.txt", "r") as file:
            lines = file.readlines()

        if lines:
            current_balance = float(lines[0].strip())
        else:
            current_balance = 0.0

        if transaction_type == "income":
            current_balance += amount
        elif transaction_type == "expense":
            if amount > current_balance:
                flash("Insufficient funds to cover expenses.")
                return redirect(url_for("transaction"))
            current_balance -= amount

        lines[0] = f"{current_balance}\n"

        transaction = Transaction(amount, category, transaction_type)
        manager.add_transaction(transaction)

        with open("transactions.txt", "w") as file:
            file.writelines(lines)
            file.write(f"{transaction_type},{category},{amount},{date}\n")

        flash(f"Transaction added! New balance: {current_balance} PLN")
    except ValueError:
        flash("Введіть правильну суму.")
    except Exception as e:
        flash(f"Помилка: {str(e)}")
    return redirect(url_for("index"))

@app.route("/recharge_balance", methods=["POST"])
def recharge_balance():
    try:
        recharge_amount = float(request.form.get("rechargeAmount"))

        if recharge_amount <= 0:
            flash("The sum must be greater than 0.")
            return redirect(url_for("recharge"))

        with open("transactions.txt", "r") as file:
            lines = file.readlines()

        if lines:
            current_balance = float(lines[0].strip())
        else:
            current_balance = 0.0

        new_balance = current_balance + recharge_amount
        lines[0] = f"{new_balance}\n"

        with open("transactions.txt", "w") as file:
            file.writelines(lines)

        flash(f"The balance has been successfully replenished! New balance: {new_balance} PLN")
    except ValueError:
        flash("Enter the correct amount.")
    except Exception as e:
        flash(f"Помилка: {str(e)}")

    return redirect(url_for("index"))

@app.route("/remove_transaction", methods=["POST"])
def remove_transaction():
    try:
        category = request.form.get("category")
        date = request.form.get("date")

        print(f"Received data: category={category}, date={date}")  # Логування даних

        with open("transactions.txt", "r") as file:
            lines = file.readlines()

        current_balance = float(lines[0].strip())
        transactions = lines[1:]

        new_balance = current_balance

        updated_transactions = []
        transaction_found = False

        for transaction in transactions:
            parts = transaction.strip().split(",")
            if len(parts) == 4 and parts[1].strip().lower() == category.lower() and parts[3].strip() == date:
                amount = float(parts[2])
                if parts[0] == "income":
                    new_balance -= amount
                elif parts[0] == "expense":
                    new_balance += amount
                transaction_found = True
            else:
                updated_transactions.append(transaction)

        if not transaction_found:
            flash("No transaction found.")
            return redirect(url_for("remove"))

        with open("transactions.txt", "w") as file:
            file.write(f"{new_balance}\n")
            file.writelines(updated_transactions)

        flash(f"Transaction deleted successfully! New balance: {new_balance} UAH")
    except Exception as e:
        flash(f"Error deleting transaction: {str(e)}")

    return redirect(url_for("index"))


@app.route("/view_transactions")
def view_transactions():
    transactions = []
    try:
        with open("transactions.txt", "r") as file:
            transactions = file.readlines()[1:]
        print("Transactions from file:", transactions)
    except Exception as e:
        flash(f"Error reading data: {e}")
    return render_template("view_transactions.html", transactions=transactions)


@app.route("/calculate_balance")
def calculate_balance():
    balance = manager.calculate_balance()
    return render_template("balance.html", balance=balance)

if __name__ == "__main__":
    app.run(debug=True)
