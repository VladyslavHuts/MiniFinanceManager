from flask import Flask, render_template, request, redirect, url_for, flash
from finance_manager.finance_manager import Transaction, FinanceManager

app = Flask(__name__)
app.secret_key = '35cv56363xv7'  # Секретний ключ для Flask

# Ініціалізуємо FinanceManager
manager = FinanceManager()

@app.route("/")
def index():
    try:
        # Зчитуємо баланс із першого рядка файлу
        with open("transactions.txt", "r") as file:
            balance = float(file.readline().strip())
    except FileNotFoundError:
        # Якщо файл не існує, встановлюємо баланс у 0
        balance = 0.0
    except ValueError:
        # Якщо формат неправильний, встановлюємо баланс у 0
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
        date = request.form.get("date")  # Зчитуємо дату з форми

        if transaction_type not in ["income", "expense"]:
            flash("Неправильний тип транзакції. Спробуйте ще раз.")
            return redirect(url_for("transaction"))

        # Зчитуємо поточний баланс із файлу
        with open("transactions.txt", "r") as file:
            lines = file.readlines()

        # Перевірка наявності балансу в першому рядку
        if lines:
            current_balance = float(lines[0].strip())
        else:
            current_balance = 0.0

        # Оновлення балансу залежно від типу транзакції
        if transaction_type == "income":
            current_balance += amount
        elif transaction_type == "expense":
            if amount > current_balance:
                flash("Недостатньо коштів для здійснення витрат.")
                return redirect(url_for("transaction"))
            current_balance -= amount

        # Оновлення першого рядка файлу (баланс)
        lines[0] = f"{current_balance}\n"

        # Створюємо об'єкт транзакції та додаємо його в менеджер
        transaction = Transaction(amount, category, transaction_type)
        manager.add_transaction(transaction)

        # Зберігаємо транзакцію в текстовому файлі разом із датою
        with open("transactions.txt", "w") as file:
            file.writelines(lines)
            file.write(f"{transaction_type},{category},{amount},{date}\n")

        flash(f"Транзакцію додано! Новий баланс: {current_balance} UAH")
    except ValueError:
        flash("Введіть правильну суму.")
    except Exception as e:
        flash(f"Помилка: {str(e)}")
    return redirect(url_for("index"))

@app.route("/recharge_balance", methods=["POST"])
def recharge_balance():
    try:
        # Отримуємо суму поповнення з форми
        recharge_amount = float(request.form.get("rechargeAmount"))

        if recharge_amount <= 0:
            flash("Сума повинна бути більше 0.")
            return redirect(url_for("recharge"))

        # Зчитуємо поточний баланс із файлу
        with open("transactions.txt", "r") as file:
            lines = file.readlines()

        # Перевірка наявності балансу в першому рядку
        if lines:
            current_balance = float(lines[0].strip())
        else:
            current_balance = 0.0

        # Оновлюємо баланс
        new_balance = current_balance + recharge_amount
        lines[0] = f"{new_balance}\n"

        # Записуємо оновлені дані назад у файл
        with open("transactions.txt", "w") as file:
            file.writelines(lines)

        flash(f"Баланс успішно поповнено! Новий баланс: {new_balance} UAH")
    except ValueError:
        flash("Введіть коректну суму.")
    except Exception as e:
        flash(f"Помилка: {str(e)}")

    return redirect(url_for("index"))


@app.route("/remove_transaction", methods=["POST"])
def remove_transaction():
    try:
        category = request.form.get("category")
        date = request.form.get("date")

        print(f"Отримано дані: category={category}, date={date}")  # Логування даних

        # Зчитуємо всі транзакції з файлу
        with open("transactions.txt", "r") as file:
            lines = file.readlines()

        # Перший рядок - це баланс
        current_balance = float(lines[0].strip())
        transactions = lines[1:]

        # Ініціалізуємо оновлений баланс
        new_balance = current_balance

        # Ініціалізуємо список для оновлених транзакцій
        updated_transactions = []
        transaction_found = False

        for transaction in transactions:
            parts = transaction.strip().split(",")
            if len(parts) == 4 and parts[1].strip().lower() == category.lower() and parts[3].strip() == date:
                amount = float(parts[2])
                # Оновлюємо баланс залежно від типу транзакції
                if parts[0] == "income":
                    new_balance -= amount
                elif parts[0] == "expense":
                    new_balance += amount
                transaction_found = True
            else:
                updated_transactions.append(transaction)

        if not transaction_found:
            flash("Транзакцію не знайдено.")
            return redirect(url_for("remove"))

        # Записуємо оновлений баланс і транзакції назад у файл
        with open("transactions.txt", "w") as file:
            file.write(f"{new_balance}\n")
            file.writelines(updated_transactions)

        flash(f"Транзакцію успішно видалено! Новий баланс: {new_balance} UAH")
    except Exception as e:
        flash(f"Помилка під час видалення транзакції: {str(e)}")

    return redirect(url_for("index"))


@app.route("/view_transactions")
def view_transactions():
    transactions = []
    try:
        with open("transactions.txt", "r") as file:
            transactions = file.readlines()[1:]  # Пропускаємо перший рядок (баланс)
        print("Транзакції з файлу:", transactions)  # Додаємо лог
    except Exception as e:
        flash(f"Помилка зчитування даних: {e}")
    return render_template("view_transactions.html", transactions=transactions)


@app.route("/calculate_balance")
def calculate_balance():
    balance = manager.calculate_balance()
    return render_template("balance.html", balance=balance)

if __name__ == "__main__":
    app.run(debug=True)
