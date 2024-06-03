import bcrypt
from utils.menus import menu


def createAccount(username, passwd, conn, mycursor):
    hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
    mycursor.execute("INSERT INTO Users(username, passwdHash) values (%s, %s)", (username, hashed))
    print("Account created!")
    conn.commit()


def loginAccount(username, passwd, conn, mycursor):
    mycursor.execute("SELECT username, passwdHash FROM Users WHERE username = %s", (username, ))

    row = mycursor.fetchone()
    if row is None:
        print("User does not exist!")
    else:
        user = row[0]
        hashedPasswd = row[1]
        if user == username:
            if bcrypt.checkpw(passwd, hashedPasswd.encode('utf-8')):
                print(f"\nWelcome, {username}!\n")
                menu(conn, mycursor, username)
            else:
                print("Incorrect username or password")
        else:
            print("User does not exist!")


def deleteAccount(username, passwd, conn, mycursor):
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
