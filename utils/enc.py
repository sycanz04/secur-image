import rsa
import os
from utils.hide import hidden
import tkinter.simpledialog


def enc(platform, passwd, imgFile, usbDir, conn, mycursor, username):
    # Generate 2048 bit pub and priv keys
    (pubKey, privKey) = rsa.newkeys(2048)
    loadedPubKey = pubKey.save_pkcs1()

    # Encrypting messages with pub key
    encryptedMessage = rsa.encrypt(passwd.encode(), pubKey)

    # Initialise encPassFile to store it temporarily
    encPassFile = f"{platform}.txt"
    with open(encPassFile, 'wb') as file:
        file.write(encryptedMessage)

    # Generating signature
    signature = rsa.sign(encryptedMessage, privKey, "SHA-256")

    # Generate path and split private key
    usbFilePath = os.path.join(usbDir, f"{username}Priv{platform}2.PEM")
    fullPrivKey = privKey.save_pkcs1()
    halfLenPrivKey = len(fullPrivKey) // 2
    privKey1 = fullPrivKey[:halfLenPrivKey]
    privKey2 = fullPrivKey[halfLenPrivKey:]

    # TODO: Store privKey2 in USB drive
    with open(usbFilePath, 'wb') as file:
        file.write(privKey2)

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
        values = (platform, loadedPubKey, privKey1, signature, userId)

        mycursor.execute(sql, values)
        conn.commit()

        # Prompt users for passphrase
        passphrase = tkinter.simpledialog.askstring(title="Passphrase", prompt="Enter passphrase:", show='*')

        success, message = hidden(platform, imgFile, encPassFile, conn, mycursor, username, passphrase)
        if success:
            return True, message
        else:
            return False, message

    except Exception as err:
        conn.rollback()
        return False, f"Error: {err}"
