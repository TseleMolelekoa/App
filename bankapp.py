import re
import sqlite3
from datetime import datetime

WELCOME_TEXT = """                         

                                                            ,___gmmmW&&&&&&&&&&&&&Wmmmm__            	
                                                         __mmW&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&s.
                                                     ,gm&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&mi
                                                    g&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&Ws_
                                                  gW&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&W.
                                                ,W&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&s
                                               g&&&&&&&&&&&&&&&&A**M&&&&**M&&&&&&&&&A********&&&&&&&&&&&&&W.
                                              d&&&&&&&&&&&&&*f~            ~~~~~~~~           ~*&&&&&&&&&&&&.
                                             i&&&&&&&&A~                                         ~M&&&&&&&&&b
                                             W&&&&&&&f                                             V&&&&&&&&&.
                                            ]&&&&&&&P                                               'V&&&&&&&W
                                           ,W&&&&&&A                                                  Y&&&&&&&i
                                           ]&&&&&&&`                                                  '&&&&&&&[
                                           ]&&&&&&!                                                    M&&&&&&&.
                                           ]&&&&&&                                                     ]&&&&&&&b
                                           d&&&&&P                                                     ]&&&&&&&&
                                           &&&&&&`                                                      &&&&&&&&
                                           &&&&&A                                                       &&&&&&&&i
                                           &&&&&[                                                       ~&&&&&&&b
                                           &&&&&                                                         ]&&&&&&&
                                           &&&&!                                                          &&&&&&&
                                           &&&&                                                           'Y&&&&&
                                           &&&!                                                             &&&&&
                                           &&&                                                              Y&&&&
                                           &&&       _mmW&&&&&&&Wms__                   __mW&&&&&&&mm.      ]&&&&
                                           &&&     g&&&*****&&&&&&&&&&W.              m&&&&&A******&&&W.     &&&&
                                        v==c&&A    d&&`         '~~~*M&&[         i    ***~~`        ~*&&i    M&&&
                                        [   Y&[    **`                 '`          i       ,______.     ~`    ]&&K_.
                                        !.  '&[         ,_mW&&&&&Wm_.                   ,gYT&&&&&&&&Wm.       ]&&f )
                                        ]c  M`       ,W&*~`&&&&&&i ~+s.               gf  ]&&A&&[  'Tf        &` --]
                                        ] \ !        'M.   Y&&W&&!  ,Z!   .       .   Vc  !&&&&&!  v`         f /  ]
                                        )   i          '\c. ~***` _=`     !       |     ~=_/~~~\_=~           [-   ]
                                        [ ,-]             '\=====~        ]       `        '~~~`              [    [
                                        ]  - \                             !             .                     ]   ]
                                        ]  . [           -        .-                       -  .,  . -`         ]-~-]
                                        ]  - [            ' -- - `                                             !. |[
                                        ] ,  [                                                                  [ -[
                                        !.  i`                                                                  [,`[
                                        [ \]                                                                   [-  [
                                        [  ]                            i                                      [ . [
                                        !. 'i                          ,!          -.                          [v  [
                                         [  [                                       -.                         [  /
                                         'i [                         -              ,                        ]  v`
                                          '=[                         [              ]                        ] /
                                            t                         ` ,W&W    i&&i !                        ]~
                                            ]                         '-___..  -,___'                         ]
                                             t                          ,..,,-. _____.                        /
                                             'i                       ,W&&&&&&]&&&&&&Ws.                      [
                                              \                    ,gW&&&&&&&&[&&&&&&&&&W.                    ]
                                               t                 ,m&&&&&&&&&&&[&&&&&&&&&&&W_                 /
                                               'i               g&&&&&&&&&&&&&!&&&&&&&&&&&&&W.               [
                                                !.            ,W&&&&&&&&&&&&&A V&&&&&&&&&&&&&&s             i~
                                                 t           g&&&&&&&&&A*f~` '~~  '~~VM&&&&&&&&W.           /
                                                  \.        d&&&&&&&f`                  'V&&&&&&W.         /
                                                   'i       &&&&&&&L '~\====_/`~\_====~~`,/M&&&&&[        i
                                                    'c      &&&&&f  \_       '~~`       v`  '&&&&!       i`
                                                     \c     '***`     ~=_.           _-`     '~~`       v`
                                                       \                 '\=_______=~                  v`
                                                        \.                                           _/
                                                          \.                                      ,/~
                                                            '\.                                 ,=
                                                              '\c                             ,v`
                                                                 ~c.                        ,/`
                                                                   'c     -_  ___. -'     _/`
                                                                     ~=_               _/~
                                                                        \=c__.    __v=~
                                                                             '~~~~


   ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗           ███████╗    ███████╗████████╗ █████╗ ██████╗ ███████╗      ██████╗  █████╗ ███╗   ██╗██╗  ██╗ █████╗ ██████╗ ██████╗ 
  ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ▄ ██╗▄██╔════╝    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝▄ ██╗▄██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗
  ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗         ██║   ██║   ██║     ████╗███████╗    ███████╗   ██║   ███████║██████╔╝███████╗ ████╗██████╔╝███████║██╔██╗ ██║█████╔╝ ███████║██████╔╝██████╔╝
  ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝         ██║   ██║   ██║    ▀╚██╔▀╚════██║    ╚════██║   ██║   ██╔══██║██╔══██╗╚════██║▀╚██╔▀██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██╔══██║██╔═══╝ ██╔═══╝ 
  ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝      ╚═╝ ███████║    ███████║   ██║   ██║  ██║██║  ██║███████║  ╚═╝ ██████╔╝██║  ██║██║ ╚████║██║  ██╗██║  ██║██║     ██║     
   ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝           ╚══════╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     


"""

CLOSE_TEXT = """
 ████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗    ██╗   ██╗ ██████╗ ██╗   ██╗    ███████╗ ██████╗ ██████╗     ██╗   ██╗███████╗██╗███╗   ██╗ ██████╗      ██████╗ ██╗   ██╗██████╗     ██████╗  █████╗ ███╗   ██╗██╗  ██╗ █████╗ ██████╗ ██████╗      ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗██╗
  ╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██╔════╝██╔═══██╗██╔══██╗    ██║   ██║██╔════╝██║████╗  ██║██╔════╝     ██╔═══██╗██║   ██║██╔══██╗    ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗    ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██║
     ██║   ███████║███████║██╔██╗ ██║█████╔╝      ╚████╔╝ ██║   ██║██║   ██║    █████╗  ██║   ██║██████╔╝    ██║   ██║███████╗██║██╔██╗ ██║██║  ███╗    ██║   ██║██║   ██║██████╔╝    ██████╔╝███████║██╔██╗ ██║█████╔╝ ███████║██████╔╝██████╔╝    ██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗  ██║
     ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗       ╚██╔╝  ██║   ██║██║   ██║    ██╔══╝  ██║   ██║██╔══██╗    ██║   ██║╚════██║██║██║╚██╗██║██║   ██║    ██║   ██║██║   ██║██╔══██╗    ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██╔══██║██╔═══╝ ██╔═══╝     ██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝  ╚═╝
     ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝    ██║     ╚██████╔╝██║  ██║    ╚██████╔╝███████║██║██║ ╚████║╚██████╔╝    ╚██████╔╝╚██████╔╝██║  ██║    ██████╔╝██║  ██║██║ ╚████║██║  ██╗██║  ██║██║     ██║██╗      ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗██╗
     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝       ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝

 """


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.account = BankAccount(self.get_balance_from_db())

    def get_balance_from_db(self):
        # Retrieve user balance from the database
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Deposit'", (self.username,))
        deposited_amount = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Withdrawal'", (self.username,))
        withdrawn_amount = cursor.fetchone()[0] or 0
        balance = deposited_amount - withdrawn_amount
        return balance

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return amount
        else:
            return "Insufficient funds!"

# Create a new SQLite database and define tables
conn = sqlite3.connect('bankapp.db')
cursor = conn.cursor()

# Define the 'users' table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')

# Define the 'transactions' table
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, transaction_type TEXT, amount REAL, transaction_time DATETIME)''')

# Commit the changes to the database 
conn.commit()



  # Get the current date and time
def write_transaction_to_db(username, transaction_type, amount, cursor, conn): 
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the transaction type is 'Check Balance'
    if transaction_type == "Check Balance":
        # Retrieve current balance and insert a transaction record with the actual balance
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Deposit'",
                       (username,))
        deposited_amount = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Withdrawal'",
                       (username,))
        withdrawn_amount = cursor.fetchone()[0] or 0
        current_balance = deposited_amount - withdrawn_amount
        cursor.execute(
            "INSERT INTO transactions (username, transaction_type, amount, transaction_time) VALUES (?, ?, ?, ?)",
            (username, transaction_type, current_balance, current_datetime))
    else:
        # Insert regular transaction record
        cursor.execute(
            "INSERT INTO transactions (username, transaction_type, amount, transaction_time) VALUES (?, ?, ?, ?)",
            (username, transaction_type, amount, current_datetime))

    # Commit the changes to the database
    conn.commit()

def write_transaction_log(username, transaction, balance):
    # Get current date and time in the specified format
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('Transaction_log.txt', 'a') as file:
        file.write(f"{current_datetime} - User: {username} - {transaction} - Balance: R{balance}\n")


def create_account():

    # Create a new user account if the username and password meet the criteria

     # Username should consist of alphanumeric characters and underscores, 4-20 characters in length
    username_pattern = r"^[a-zA-Z0-9_]{4,20}$" 
    
    # Password should contain at least one lowercase, one uppercase, one digit, and be at least 8 characters long
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$"  
    while True:
        username = input("Enter your username: ")
        if not re.match(username_pattern, username):
            print("Invalid username format. Username should consist of alphanumeric characters and underscores, 4-20 characters in length.")
        else:
            break

    while True:
        password = input("Enter your password: ")
        if not re.match(password_pattern, password):
            print("Invalid password format. Password should contain at least one lowercase, one uppercase, one digit, and be at least 8 characters long.")
        else:
            break

    # Check if the username already exists in the database
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Username already exists. Please choose a different username.")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Account created successfully!")

def login():
    # Handle user login and retrieve user data from the database
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user_data = cursor.fetchone()

    if user_data:
        print("Login successful!")
        # Fetch and display the current balance immediately after login
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Deposit'",
            (username,))
        deposited_amount = cursor.fetchone()[0] or 0
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE username=? AND transaction_type='Withdrawal'",
            (username,))
        withdrawn_amount = cursor.fetchone()[0] or 0
        current_balance = deposited_amount - withdrawn_amount
        print("Your current balance: R", current_balance)

        # Return the User object with the username, password, and current balance
        return User(username, password)
    else:
        print("Invalid username or password. Please try again.")
        return None
def main():
    while True:
        try:
            # User interface
            print(WELCOME_TEXT)
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
                                    if amount < 0:
                                        print("Invalid withdrawal aount. PLeae enter a positive number")
                                    else:
                                         withdrawn_amount  = user.account.withdraw(amount)
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
                                print(f"Transaction ID: {transaction[0]}, Type: {transaction[2]}, Amount: R{transaction[3]}, Time: {transaction[4]}")
                        elif option == "4":
                            # Logout
                            print("Logout successful!")
                            break
                        else:
                            print("Invalid choice! Please try again.")
            elif choice == "3":
                # Exit
                print(CLOSE_TEXT)
                break
            else:
                print("Invalid choice! Please try again.")

        except Exception as e:
            print("An unexpected error occurred:", e)

if __name__ == "__main__":
    main()

# Close the database connection
conn.close()


