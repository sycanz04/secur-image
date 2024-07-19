import bcrypt
import pyotp


def deleteImage(passwd, conn, mycursor, username):
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
                    mycursor.execute("SELECT userId, photo FROM Users WHERE username = %s AND photoId = %s", (username, id))
                    row = mycursor.fetchone()
                    if row is None:
                        print("Image does not exist!")
                    else:
                        mycursor.execute("DELETE FROM Images WHERE userId = (SELECT userId FROM Users WHERE username = %s", (username, ))
                        conn.commit()
                        print(f"Succefully removed {username}'s account!")
                else:
                    print("Invalid OTP. Please try again.")
            else:
                print("Incorrect username or password")
        else:
            print("User does not exist!")
