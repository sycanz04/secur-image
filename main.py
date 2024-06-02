#! /usr/bin/env python3
from utils.enc import enc
from utils.dec import dec
from utils.ver import ver
from utils.hide import hid
from utils.account import loginAccount, createAccount, deleteAccount
import cred
import mysql.connector


conn = mysql.connector.connect(
    host=cred.hostname,
    user=cred.username,
    passwd=cred.password,
    database=cred.databaseName
)
mycursor = conn.cursor()


def menu():
    print("""
Options
1. Generate
2. Decrypt
3. Verify
4. Hide
5. Quit\n
""")
    prompt = input("What do you want to do? ")

    if prompt == "1":
        platform = input("Platform: ")
        enc(platform)
    elif prompt == "2":
        platform = input("Platform: ")
        dec(platform)
    elif prompt == "3":
        platform = input("Platform: ")
        ver(platform)
    elif prompt == "4":
        hid()
    elif prompt == "5":
        print("Goodbye!")
        quit()
    else:
        print("\nInvalid option. Pick again!\n")
        main()


def main():
    print("""
Account Options
1. Login
2. Signup
3. Delete
4. Quit
""")
    prompt = input("What do you want to do? ")

    if prompt == "1":
        username = input("Username: ")
        passwd = input("Password: ").encode('utf-8')
        loginAccount(username, passwd, conn, mycursor)
    elif prompt == "2":
        username = input("Username: ")
        passwd = input("Password: ").encode('utf-8')
        createAccount(username, passwd, conn, mycursor)
    elif prompt == "3":
        username = input("Username: ")
        passwd = input("Password: ").encode('utf-8')
        deleteAccount(username, passwd, conn, mycursor)
    elif prompt == "4":
        print("Goodbye!")
        quit()
    else:
        print("\nInvalid option. Pick again!\n")
        main()


if __name__ == "__main__":
    main()
