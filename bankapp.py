# File names for data storage
bank_data_file = "Bank_Data.txt"
transaction_log_file = "Transaction_log.txt"

# Function to display the current balance
def display_balance(balance):
    print(f"Current Balance: R{balance:.2f}")

# Function to make a deposit
def make_deposit(balance, amount):
    balance += amount
    with open(transaction_log_file, "a") as transaction_file:
        transaction_file.write(f"Deposit: +R{amount:.2f}\n")
    display_balance(balance)
    return balance

# Function to make a withdrawal
def make_withdrawal(balance, amount):
    if amount <= balance:
        balance -= amount
        with open(transaction_log_file, "a") as transaction_file:
            transaction_file.write(f"Withdrawal: -R{amount:.2f}\n")
        display_balance(balance)
        return balance
    else:
        print("Insufficient funds. Withdrawal canceled.")
        return balance

# Function for user registration
def register():
    print("User Registration")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    with open(bank_data_file, "a") as data_file:
        data_file.write(f"{username},{password}\n")
    print("Registration successful!")

# Function for user login
def login():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    with open(bank_data_file, "r") as data_file:
        for line in data_file:
            existing_username, existing_password = line.strip().split(",")
            if username == existing_username and password == existing_password:
                print("Login successful!")
                return username
    print("Invalid username or password. Please try again.")
    return None

# Main application loop
while True:
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        register()
    elif choice == "2":
        username = login()
        if username:
            balance = 0.0  # Initialize user's balance
            while True:
                print("1. Make a Transaction")
                print("2. View Transaction History")
                print("3. Logout")
                option = input("Enter your choice: ")

                if option == "1":
                    print("1. Deposit")
                    print("2. Withdraw")
                    transaction_type = input("Enter the transaction type (1 or 2): ")

                    if transaction_type == "1":
                        display_balance(balance)
                        print("How much would you like to deposit in Rands?")
                        try:
                            amount = float(input())
                            if amount > 0:
                                balance = make_deposit(balance, amount)
                            else:
                                print("Invalid deposit amount.")
                        except ValueError:
                            print("Invalid input. Please enter a valid amount.")
                    elif transaction_type == "2":
                        display_balance(balance)
                        print("How much would you like to withdraw in Rands?")
                        try:
                            amount = float(input())
                            if amount > 0:
                                balance = make_withdrawal(balance, amount)
                        except ValueError:
                            print("Invalid input. Please enter a valid amount.")
                    else:
                        print("Invalid transaction type.")
                elif option == "2":
                    print("Transaction History:")
                    with open(transaction_log_file, "r") as transaction_file:
                        transaction_history = transaction_file.read()
                        print(transaction_history)
                elif option == "3":
                    print("Logout successful!")
                    break
                else:
                    print("Invalid choice. Please try again.")
    elif choice == "3":
        print("Thank you for using the bank app. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
