# ----------------------- IMPORTS -----------------------

import json
import os
import time
import random
from os.path import exists


# ----------------------- CONSTANT -----------------------

FILE_NAME = "banking_system.json"


# ----------------------- DATABASE -----------------------

def get_users_data():
    """
    Reads the bank information from the data file.
    """
    # assume none existent file as empty file
    if not exists(FILE_NAME):
        return {}
    f = open(FILE_NAME, "r")
    data = f.read()
    # convert string json to python object
    return json.loads(data)


def set_users_data(data):
    """
    Writes the bank information into the data file
    """
    f = open(FILE_NAME, "w")
    json_data = json.dumps(data)
    f.write(json_data)


def sort_by_money():
    """
    Sorts the user's data by balance decrease
    """
    users = get_users_data()

    sorted_database = sorted(users.items(), key=lambda x: x[1]['balance'])
    return sorted_database[::-1]


# ----------------------- ACCOUNT NUMBER -----------------------

def generate_account_number():
    """
    Generate an account number, 16 digits are generated randomly,
    checks unique of number
    """
    users = get_users_data()

    gen_num = ""
    for _ in range(1, 17):
        random_num = random.randint(1, 9)
        gen_num += str(random_num)
    while gen_num in users.keys():
        for _ in range(1, 17):
            random_num = random.randint(1, 9)
            gen_num += str(random_num)
    else:
        return gen_num


# ----------------------- CREATE A NEW ACCOUNT -----------------------

def create_new_account(name):
    """
    Creates a new account with the given name
    """
    users = get_users_data()

    account_number = generate_account_number()
    users[account_number] = {
        "name": name,
        "balance": 0,
    }

    set_users_data(users)
    return account_number


# ----------------------- DELETE AN ACCOUNT -----------------------

def delete_account(account_number):
    """
    Deletes an account if exists, otherwise warns
    about the absence of an account number
    """
    users = get_users_data()

    if account_number not in users:
        print("Did not found the account with number: " + account_number)
        return
    del users[account_number]
    set_users_data(users)
    print("ACCOUNT NUMBER REMOVED!")


# ----------------------- CHECK THE BALANCE OF ACCOUNT -----------------------

def check_the_balance(account_number):
    """
    Checks the balance of account if it exists, otherwise warns
    about the absence of an account number
    """
    users = get_users_data()

    if account_number not in users:
        print("Did not found the account with number: " + account_number)
        return
    else:
        balance = users[account_number]["balance"]
        return balance


# ----------------------- ADD MONEY -----------------------

def add_money(account_number, amount):
    """
    Adds amount to the account if it exists and returns the
    total amount,otherwise warns about the absence of an
    account number
    """
    users = get_users_data()

    if account_number not in users:
        print("Did not found the account with number: " + account_number)
        return

    users[account_number]["balance"] += amount
    set_users_data(users)
    total_amount = users[account_number]["balance"]
    print(f"Your total amount is: {total_amount}$")


# ----------------------- TRANSACTION -----------------------

def perform_transaction(sender_account_number, receiver_account_number, amount):
    """
    Given two account numbers and a transaction amount, this will move
    the money from the sender account to the recipient account.
    """
    users = get_users_data()

    if sender_account_number not in users:
        print("Did not found the account with number: " + sender_account_number)
        return

    if receiver_account_number not in users:
        print("Did not found the account with number: " + receiver_account_number)
        return

    if users[sender_account_number]["balance"] < amount:
        print(f"Your account balance is not enough")
        return

    users[sender_account_number]["balance"] -= amount
    users[receiver_account_number]["balance"] += amount

    set_users_data(users)
    sender = users[sender_account_number]["name"]
    receiver = users[receiver_account_number]["name"]
    print(f"Transferred {amount}$ from account {sender} to {receiver}")


# ----------------------- DISPLAY USER'S LIST -----------------------

def show_all_accounts(account_list):
    """
    Displays all the users one after the other, sorted by balance
    """

    for i in range(len(account_list)):
        name = account_list[i][1]["name"]
        print(f"Name = {name}")
        print(f"Account number = {account_list[i][0]}")
        balance = account_list[i][1]["balance"]
        print(f"Balance = {balance}\n")


# ----------------------- FOR TERMINAL INTERFACE -----------------------

def clean_terminal_screen():
    """
    Cleans the terminal screen by performing a system
    clear command. Cls on windows and Clear on UNIX ones.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# ----------------------- DISPLAY MENU -----------------------

def main_menu():
    """
    Displays the welcome menu and asks the user for a
    command to perform (which then performs).
    This also acts as the UI and receives the information
    regarding of the respective functions.
    """

    clean_terminal_screen()

    print()
    print("MAIN MENU")
    print("1. NEW ACCOUNT")
    print("2. CHECK THE BALANCE")
    print("3. ADD MONEY")
    print("4. PERFORM TRANSACTION")
    print("5. VIEW USER'S LIST BY BALANCE DECREASE")
    print("6. DELETE ACCOUNT")
    print("7. EXIT")

    user_choice = input("Enter your choice please (1-7): ")

    clean_terminal_screen()
    if user_choice == '1':
        print('_______ CREATING AN ACCOUNT _______')
        user_name = input("Enter your full name please: ")
        account_number = create_new_account(user_name)
        print("--------------------------------")
        print("ACCOUNT SUCCESSFULLY CREATED!")
        print(f"YOUR ACCOUNT NUMBER IS: {account_number}")
        time.sleep(1)

    if user_choice == "2":
        print('_______ CHECKING THE BALANCE _______')
        account_number = input("Please enter account number for check: ")
        balance = check_the_balance(account_number)
        print(f"Your account balance is: {balance}$")

    if user_choice == "3":
        print('_______ ADDING THE BALANCE _______')
        account_number = input("Please enter account number for add a money: ")
        print("Enter amount to be added")
        amount = float(input("Amount added: "))
        add_money(account_number, amount)

    if user_choice == "4":
        print('_______ PERFORMING TRANSACTION _______')
        sender = input("Sender's Account Number: ")
        receiver = input("Recipient's Account Number: ")
        amount = float(input("Transaction Amount: "))
        perform_transaction(sender, receiver, amount)

    if user_choice == "5":
        print('_______ SHOWING ALL ACCOUNTS _______')
        account_list = sort_by_money()
        show_all_accounts(account_list)

    if user_choice == "6":
        print('_______ DELETING AN ACCOUNT _______')
        account_number = input("Please enter account number for delete: ")
        delete_account(account_number)

    if user_choice == '7':
        print("THANK YOU FOR USING OUR SERVICE!")
        time.sleep(1)
        quit()

    if user_choice not in "12345678":
        print("--------------------------------")
        print("INVALID OPTION,PLEASE TRY AGAIN!")
        time.sleep(1)

    input("PRESS ENTER TO CONTINUE ")
    print()


print("----------------------")
print("BANK MANAGEMENT SYSTEM")
print("----------------------")
time.sleep(1)

# ----------------------- MAIN -----------------------

while True:
    main_menu()
