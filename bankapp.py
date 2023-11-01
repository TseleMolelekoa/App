import sqlite3
from datetime import datetime
import re
import bcrypt

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.account = BankAccount(self.get_balance_from_db())

    def get_balance_from_db(self):
        # Retrieve user balance from the database
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Deposit'",
                       (self.username,))
        deposited_amount = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Withdrawal'",
                       (self.username,))
        withdrawn_amount = cursor.fetchone()[0] or 0
        balance = deposited_amount - withdrawn_amount
        return balance


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:  # Disallow negative deposits
            self.balance += amount
            return amount
        else:
            return "Invalid deposit amount!"

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:  # Disallow negative and excessive withdrawals
            self.balance -= amount
            return amount
        elif amount <= 0:
            return "Invalid withdrawal amount!"
        else:
            return "Insufficient funds!"

conn = sqlite3.connect('bankapp.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, transaction_type TEXT, amount REAL, transaction_time DATETIME)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS balance
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, balance REAL)''')

conn.commit()


def write_transaction_to_db(username, transaction_type, amount, cursor, conn):
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if transaction_type == "Check Balance":
        # Retrieve current balance and insert a transaction record with the actual balance
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Deposit'", (username,))
        deposited_amount = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Withdrawal'", (username,))
        withdrawn_amount = cursor.fetchone()[0] or 0
        current_balance = deposited_amount - withdrawn_amount

        # Insert the transaction record with the actual balance into the transactions table
        cursor.execute(
            "INSERT INTO transactions (username, transaction_type, amount, transaction_time) VALUES (?, ?, ?, ?)",
            (username, transaction_type, current_balance, current_datetime))

    else:
        # Insert regular transaction record
        cursor.execute(
            "INSERT INTO transactions (username, transaction_type, amount, transaction_time) VALUES (?, ?, ?, ?)",
            (username, transaction_type, amount, current_datetime))

        # Update balance table with the new balance after the transaction
        cursor.execute("SELECT balance FROM balance WHERE username=?", (username,))
        current_balance = cursor.fetchone()
        if current_balance:
            current_balance = current_balance[0]
        else:
            current_balance = 0

        if transaction_type == "Deposit":
            current_balance += amount
        elif transaction_type == "Withdrawal":
            current_balance -= amount

        # Update the balance table with the new balance
        cursor.execute("INSERT OR REPLACE INTO balance (username, balance) VALUES (?, ?)", (username, current_balance))

    # Commit the changes to the database
    conn.commit()
def write_transaction_log(username, transaction, amount, balance):
    # Get current date and time in the specified format
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('TransactionLog.txt', 'a') as file:
        if transaction == "Logout":
            file.write(f"Transaction history for {username}:\n")
            file.write(f"Withdraw: {amount}\n")
            file.write(f"Deposit: {amount}\n")
            file.write(f"Check Balance: {balance}\n")
            file.write(f"{'=' * 40}\n")
        else:
            file.write(f"{current_datetime} - User: {username} - {transaction} - Amount: R{amount} - Balance: R{balance}\n")


def is_valid_password(password):
    # Password must be at least 8 characters long
    # It must contain at least one uppercase letter, one lowercase letter, and one special character
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    return re.match(regex, password) is not None

def create_account():
    # Create a new user account and insert it into the database
    username = input("Enter your username: ")
    while True:
        password = input("Enter your password: ")
        if is_valid_password(password):
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            break
        else:
            print("Invalid password! Password must be at least 8 characters with at least one uppercase letter, one lowercase letter, and one special character.")
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    print("Account created successfully!")


def login():
    # Handle user login and retrieve user data from the database
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()

    if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[2].encode('utf-8')):
        print("Login successful!")
        user = User(user_data[1], user_data[2])
        print("Current Balance: R", user.account.balance)  # Display current balance after login
        return user
    else:
        print("Invalid username or password. Please try again.")
        return None
def main():
    while True:
        try:
            # User interface
            print("=================================================\n----------Welcome to the 5STARS_BankApp!--------- \n=================================================")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                create_account()
            elif choice == "2":
                user = login()
                if user:
                    while True:
                        # Banking operations menu
                        print("1. Check Balance")
                        print("2. Make a Transaction")
                        print("3. View Transaction History")
                        print("4. Logout")
                        option = input("Enter your choice: ")

                        if option == "1":
                            # Check Balance operation
                            cursor.execute(
                                "SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Deposit'",
                                (user.username,))
                            deposited_amount = cursor.fetchone()[0] or 0
                            cursor.execute(
                                "SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Withdrawal'",
                                (user.username,))
                            withdrawn_amount = cursor.fetchone()[0] or 0
                            current_balance = deposited_amount - withdrawn_amount
                            print("Your balance: R", current_balance)

                            # Call write_transaction_to_db with cursor and conn variables
                            write_transaction_to_db(user.username, "Check Balance", current_balance, cursor, conn)
                            write_transaction_log(user.username, "Check Balance",
                                                  current_balance)  # Log the transaction
                        # Log the transaction
                        elif option == "2":
                            # Make a transaction
                            print("Current Balance: R", user.account.balance)
                            make_transaction = input(
                                "Would you like to make a transaction? (Yes or No): ").strip().lower()
                            if make_transaction == "yes":
                                transaction_type = input(
                                    "Would you like to make a deposit or withdrawal? (Deposit or Withdrawal): ").strip().lower()
                                if transaction_type == "deposit":
                                    amount = float(input("How much would you like to deposit? R"))
                                    deposited_amount = user.account.deposit(amount)
                                    # Pass cursor and conn to the write_transaction_to_db function
                                    write_transaction_to_db(user.username, "Deposit", deposited_amount, cursor, conn)
                                    write_transaction_log(user.username, "Deposit",
                                                          deposited_amount)  # Log the transaction
                                    print("Deposit successful! Your new balance: R", user.account.balance)
                                elif transaction_type == "withdrawal":
                                    amount = float(input("How much would you like to withdraw? R"))
                                    withdrawn_amount = user.account.withdraw(amount)
                                    if isinstance(withdrawn_amount, str):
                                        print(withdrawn_amount)
                                    else:
                                        # Pass cursor and conn to the write_transaction_to_db function
                                        write_transaction_to_db(user.username, "Withdrawal", withdrawn_amount, cursor,
                                                                conn)
                                        write_transaction_log(user.username, "Withdrawal",
                                                              withdrawn_amount)  # Log the transaction
                                        print("Withdrawal successful! Your new balance: R", user.account.balance)
                                else:
                                    print("Invalid transaction type! Please try again.")
                            elif make_transaction == "no":
                                print("No transaction made.")
                            else:
                                print("Invalid choice! Please enter Yes or No.")
                        elif option == "3":
                            # View transaction history
                            print("Transaction History:")
                            cursor.execute("SELECT * FROM transactions WHERE username=?", (user.username,))
                            transactions = cursor.fetchall()
                            for transaction in transactions:
                                print(
                                    f"Transaction ID: {transaction[0]}, Type: {transaction[2]}, Amount: R{transaction[3]}, Time: {transaction[4]}")
                        elif option == "4":
                            # Logout
                            print("Logout successful!")
                            break
                        else:
                            print("Invalid choice! Please try again.")
            elif choice == "3":
                # Exit
                print("Thank you for using 5STARS_BankApp. Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")

        except Exception as e:
            print("An unexpected error occurred:", e)

if __name__ == "__main__":
    main()

# Close the database connection
conn.close()
