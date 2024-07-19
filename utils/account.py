import bcrypt
import pyotp
import qrcode
from utils.menus import menu


def loginAccount(username, passwd, conn, mycursor):
    mycursor.execute("SELECT username, passwdHash, secretKey FROM Users WHERE username = %s", (username, ))

    row = mycursor.fetchone()
    if row is None:
        print("User does not exist!")
    else:
        user = row[0]
        hashedPasswd = row[1]
        secretKey = row[2]

        totp = pyotp.TOTP(secretKey)

        if user == username:
            if bcrypt.checkpw(passwd, hashedPasswd.encode('utf-8')):
                otpPrompt = input("Enter OTP code: ")

                if totp.verify(otpPrompt):
                    print(f"\nWelcome, {username}!\n")
                    menu(conn, mycursor, username)
                else:
                    print("Invalid OTP. Please try again.")
            else:
                print("Incorrect username or password")
        else:
            print("User does not exist!")

def createAccount(username, passwd, conn, mycursor):
    try:
        hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
        secretKey = pyotp.random_base32()

        uri = pyotp.totp.TOTP(secretKey).provisioning_uri(name=username, issuer_name="securImage")
        qrcode.make(uri).save("totp.png")

        mycursor.execute("INSERT INTO Users(username, passwdHash, secretKey) values (%s, %s, %s)", (username, hashed, secretKey))
        conn.commit()
        return True
    except Exception as e:
        return False

def deleteAccount(username, passwd, conn, mycursor):
    try:
        mycursor.execute("SELECT username, passwdHash FROM Users WHERE username = %s", (username,))
        row = mycursor.fetchone()

        if row is None:
            return False, "User does not exist!"
        else:
            user = row[0]
            hashedPasswd = row[1]
            if user == username:
                if bcrypt.checkpw(passwd, hashedPasswd.encode('utf-8')):
                    mycursor.execute("DELETE FROM Users WHERE username = %s", (username,))
                    conn.commit()
                    return True, f"Succefully removed {username}'s account!"
                else:
                    return False, "Incorrect username or password"
            else:
                return False, "User does not exist!"
    except Exception as e:
        return False, f"Error deleting account: {e}"
