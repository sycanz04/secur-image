#! /usr/bin/env python3
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

mycursor.execute("""CREATE TABLE IF NOT EXISTS Users
                    (userId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                     username VARCHAR(50) NOT NULL,
                     passwdHash VARCHAR(255) NOT NULL,
                     secretKey VARCHAR(255) NOT NULL);""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS Images
                    (photoId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                     platform VARCHAR(50) NOT NULL,
                     photo LONGBLOB NOT NULL,
                     userId INT NOT NULL,
                     FOREIGN KEY(userId) REFERENCES Users(userId));""")


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
