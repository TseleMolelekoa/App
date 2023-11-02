from datetime import datetime

# Dictionary to store user data (username as key, list of user data as values)
user_data = {}

# Function to display the current balance
def display_balance(username):
    user = user_data[username][0]  # Get the first user with the provided username
    balance = user["balance"]
    print(f"Current Balance for {username}: R{balance:.2f}")

# Function to log a transaction
def log_transaction(username, transaction_type, amount):
    user = user_data[username][0]  # Get the first user with the provided username

    if "transactions" not in user:
        user["transactions"] = []

    current_datetime = datetime.now().strftime("%Y-%m-d %H:%M:%S")
    transaction = {
        "Date": current_datetime,
        "Type": transaction_type,
        "Amount": amount
    }
    user["transactions"].append(transaction)

    # Write the transaction to the transaction log file
    with open('transaction_log.txt', 'a') as log_file:
        log_file.write(f"User: {username}, Date: {transaction['Date']}, Type: {transaction['Type']}, Amount: R{transaction['Amount']:.2f}\n")

# Function to check if an amount is greater than or equal to 20 and is a multiple of 10
def is_valid_amount(amount):
    return amount >= 20 and amount % 10 == 0

# Function to make a deposit
def make_deposit(username, amount):
    if is_valid_amount(amount):
        user = user_data[username][0]  # Get the first user with the provided username
        user["balance"] += amount
        log_transaction(username, "Deposit", amount)
        display_balance(username)
    else:
        print("Invalid deposit amount. Deposit amount must be greater than or equal to 20 and a multiple of 10.")

# Function to make a withdrawal
def make_withdrawal(username, amount):
    if is_valid_amount(amount):
        user = user_data[username][0]  # Get the first user with the provided username

        if amount <= user["balance"]:
            user["balance"] -= amount
            log_transaction(username, "Withdrawal", amount)
            display_balance(username)
        else:
            print("Invalid withdrawal amount. Withdrawal amount must be within your balance.")
    else:
        print("Invalid withdrawal amount. Withdrawal amount must be greater than or equal to 20 and a multiple of 10.")

# Function to save user data to the Bank_Data.txt file
def save_user_data():
    with open('Bank_Data.txt', 'w') as data_file:
        for username, users in user_data.items():
            for user in users:
                data_file.write(f"{username} {user['password']}\n")

# Function to load user data from the Bank_Data.txt file
def load_user_data():
    try:
        with open('Bank_Data.txt', 'r') as data_file:
            for line in data_file:
                parts = line.split()
                if len(parts) >= 3:
                    username = parts[0]
                    password = parts[1]

                    user = {
                        "password": password,
                        "balance": 0.0,
                        "transactions": []
                    }
                    
                    if username in user_data:
                        user_data[username].append(user)
                    else:
                        user_data[username] = [user]
    except FileNotFoundError:
        # Create the file if it doesn't exist
        open('Bank_Data.txt', 'w').close()

load_user_data()  # Load user data from Bank_Data.txt

# Function for user registration
def register():
    print("Register here:")
    username = input("Enter your username: ").strip()

    if not username:
        print("Empty spaces as username are not allowed.")
        return  # Exit the registration function

    password = input("Enter your password: ").strip()

    if username in user_data:
        # User with this username already exists, add a new user with the provided password
        user_data[username].append({
            "password": password,
            "balance": 0.0,
            "transactions": []
        })
        print("Registration successful!")
    else:
        # User with this username doesn't exist, create a new entry with the username and password
        user_data[username] = [{
            "password": password,
            "balance": 0.0,
            "transactions": []
        }]
        print("Registration successful!")

    # Save user data to Bank_Data.txt
    save_user_data()

# Function for user login
def login():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if username in user_data:
        for user in user_data[username]:
            if user["password"] == password:
                print("Login successful!")
                return username

    print("Invalid username or password. Please try again.")
    return None

# Main application loop
print("*****Welcome to Five Stars Bank App*****")
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
                            if is_valid_amount(amount):
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
                            make_withdrawal(username, amount)
                        except ValueError:
                            print("Invalid input. Please enter a valid amount.")
                    else:
                        print("Invalid transaction type.")
                elif option == "2":
                    if username in user_data:
                        print("Transaction History for", username + ":")
                        for user in user_data[username]:
                            for transaction in user["transactions"]:
                                print(f"Date: {transaction['Date']}, Type: {transaction['Type']}, Amount: R{transaction['Amount']:.2f}")
                    else:
                        print("No transaction history available.")
                elif option == "3":
                    print("Logout successful!")
                    break
                else:
                    print("Invalid choice. Please try again.")
    elif choice == "3":
        print("Thank you for using the Five Stars Bank App. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
