#! /usr/bin/env python3
from utils.enc import enc
from utils.dec import dec
from utils.ver import ver
from utils.hide import hid
import cred
import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host=cred.hostname,
    user=cred.username,
    passwd=cred.password,
    database=cred.databaseName
)
mycursor = conn.cursor()


def createAccount():
    username = input("Username: ")
    passwd = input("Password: ")
    hashed = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    mycursor.execute("INSERT INTO Users(username, passwdHash) values (%s, %s)", (username, hashed))
    conn.commit()


def loginAccount():
    username = input("Username: ")
    passwd = input("Password: ").encode('utf-8')
    mycursor.execute("SELECT username, passwdHash FROM Users WHERE username = %s", (username))

    row = mycursor.fetchone()
    if row is None:
        print("User does not exist!")
    else:
        user = row[0]
        hashedPasswd = row[1]
        if user == username:
            if bcrypt.checkpw(passwd, hashedPasswd.encode('utf-8')):
                print(f"Welcome, {username}!")
            else:
                print("Incorrect username or password")
        else:
            print("User does not exist!")


def deleteAccount():
    username = input("Username: ")
    passwd = input("Password: ").encode('utf-8')
    mycursor.execute("SELECT username, passwdHash FROM Users WHERE username = %s", (username,))

    row = mycursor.fetchone()
    if row is None:
        print("User does not exist!")
    else:
        user = row[0]
        hashedPasswd = row[1]
        if user == username:
            if bcrypt.checkpw(passwd, hashedPasswd.encode('utf-8')):
                mycursor.execute("DELETE FROM Users WHERE username = %s", (username,))
                conn.commit()
                print(f"Succefully removed {username}'s account!")
            else:
                print("Incorrect username or password")
        else:
            print("User does not exist!")



def main():
    deleteAccount()
#     print("""
# Options
# 1. Generate
# 2. Decrypt
# 3. Verify
# 4. Hide
# 5. Quit\n
# """)
#     prompt = input("What do you want to do? ")
# 
#     if prompt == "1":
#         platform = input("Platform: ")
#         enc(platform)
#     elif prompt == "2":
#         platform = input("Platform: ")
#         dec(platform)
#     elif prompt == "3":
#         platform = input("Platform: ")
#         ver(platform)
#     elif prompt == "4":
#         hid()
#     elif prompt == "5":
#         print("Goodbye!")
#         quit()
#     else:
#         print("\nInvalid option. Pick again!\n")
#         main()


if __name__ == "__main__":
    main()

mycursor.close()
conn.close()

