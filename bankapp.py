from datetime import datetime

# Dictionary to store user data (username as key, password, balance, and transaction history as values)
user_data = {}

# Function to display the current balance
def display_balance(username):
    balance = user_data[username]["balance"]
    print(f"Current Balance for {username}: R{balance:.2f}")

# Function to log a transaction
def log_transaction(username, transaction_type, amount):
    if "transactions" not in user_data[username]:
        user_data[username]["transactions"] = []

    current_datetime = datetime.now().strftime("%Y-%m-d %H:%M:%S")
    transaction = {
        "Date": current_datetime,
        "Type": transaction_type,
        "Amount": amount
    }
    user_data[username]["transactions"].append(transaction)

    # Write the transaction to the transaction log file
    with open('transaction_log.txt', 'a') as log_file:
        log_file.write(f"User: {username}, Date: {transaction['Date']}, Type: {transaction['Type']}, Amount: R{transaction['Amount']:.2f}\n")

# Function to make a deposit
def make_deposit(username, amount):
    user_data[username]["balance"] += amount
    log_transaction(username, "Deposit", amount)
    display_balance(username)

# Function to make a withdrawal
def make_withdrawal(username, amount):
    if amount <= user_data[username]["balance"]:
        user_data[username]["balance"] -= amount
        log_transaction(username, "Withdrawal", amount)
        display_balance(username)
    else:
        print("Insufficient funds. Withdrawal canceled.")

# Function to save user data to the Bank_Data.txt file
def save_user_data():
    with open('Bank_Data.txt', 'w') as data_file:
        for username, data in user_data.items():
            data_file.write(f"{username} {data['password']}\n")

# Function to load user data from the Bank_Data.txt file
def load_user_data():
    try:
        with open('Bank_Data.txt', 'r') as data_file:
            for line in data_file:
                parts = line.split()
                if len(parts) >= 3:
                    username = parts[0]
                    password = parts[1]
                    
                    user_data[username] = {
                        "password": password,
                        "transactions": []
                    }
    except FileNotFoundError:
        # Create the file if it doesn't exist
        open('Bank_Data.txt', 'w').close()

load_user_data()  # Load user data from Bank_Data.txt

# Function for user registration
def register():
    print(" register here:")
    username = input("Enter your username: ").strip()
    
    if not username:
        print("Empty spaces as username are not allowed.")
        return  # Exit the registration function

    password = input("Enter your password: ").strip()

    if username in user_data:
        if user_data[username]["password"] == password:
            print("Username and password combination already exists. Registration failed.")
        else:
            print("Username already exists, but you can use a different password.")
    else:
        user_data[username] = {
            "password": password,
            "balance": 0.0,
            "transactions": []
        }
        print("Registration successful!")

    # Save user data to Bank_Data.txt
    save_user_data()

# Function for user login
def login():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if username in user_data:
        if user_data[username]["password"] == password:
            print("Login successful!")
            return username

    print("Invalid username or password. Please try again.")
    return None

# Main application loop
print("*****Welcome to Five Stars bank App*****")
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
                        display_balance(username)
                        print("How much would you like to deposit?")
                        try:
                            amount = float(input())
                            if amount >= 20:
                                make_deposit(username, amount)
                            else:
                                print("Invalid deposit amount.")
                        except ValueError:
                            print("Invalid input. Please enter a valid amount.")
                    elif transaction_type == "2":
                        display_balance(username)
                        print("How much would you like to withdraw?")
                        try:
                            amount = float(input())
                            if amount >= 20:
                                make_withdrawal(username, amount)
                            else:
                                print("Invalid withdrawal amount.")
                        except ValueError:
                            print("Invalid input. Please enter a valid amount.")
                    else:
                        print("Invalid transaction type.")
                elif option == "2":
                    if "transactions" in user_data[username]:
                        print("Transaction History for", username + ":")
                        for transaction in user_data[username]["transactions"]:
                            print(f"Date: {transaction['Date']}, Type: {transaction['Type']}, Amount: R{transaction['Amount']:.2f}")
                    else:
                        print("No transaction history available.")
                elif option == "3":
                    print("Logout successful!")
                    break
                else:
                    print("Invalid choice. Please try again.")
    elif choice == "3":
        print("Thank you for using the 5 Stars Bank App. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
