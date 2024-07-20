import rsa
import os
from utils.hide import hidden
import tkinter.simpledialog


def enc(platform, passwd, imgFile, conn, mycursor, username):
    # Generate 2048 bit pub and priv keys
    (pubKey, privKey) = rsa.newkeys(2048)

    # Encrypting messages with pub key
    encryptedMessage = rsa.encrypt(passwd.encode(), pubKey)

    # Initialise encPassFile to store it temporarily
    encPassFile = f"{platform}.txt"
    with open(encPassFile, 'wb') as file:
        file.write(encryptedMessage)

    # Generating signature
    signature = rsa.sign(encryptedMessage, privKey, "SHA-256")

    try:
        # Query userId
        mycursor.execute("SELECT userId FROM Users WHERE username = %s", (username,))
        rows = mycursor.fetchone()

        if rows is None:
            return False, "User not found!"
        else:
            userId = rows[0]

        # Insert values into database
        sql = "INSERT INTO `keys` (platform, pubKey, privKey, signature, userId) VALUES (%s, %s, %s, %s, %s)"
        values = (platform, pubKey.save_pkcs1(), privKey.save_pkcs1(), signature, userId)

        mycursor.execute(sql, values)
        conn.commit()

        # Prompt users for passphrase
        passphrase = tkinter.simpledialog.askstring(title="Passphrase", prompt="Enter passphrase:", show='*')

        success, message = hidden(platform, imgFile, encPassFile, conn, mycursor, username, passphrase)
        if not success:
            return False, message

        return True, "Insertion successful"

    except Exception as err:
        conn.rollback()
        return False, f"Error: {err}"
