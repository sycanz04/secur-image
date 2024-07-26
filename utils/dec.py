import rsa
import os
from utils.hide import extract
import tkinter.simpledialog


def dec(platform, usbDir, mycursor, username):
    # Query userId
    mycursor.execute("SELECT userId FROM Users WHERE username = %s", (username,))
    userIdRows = mycursor.fetchone()

    if userIdRows is None:
        return False, "User not found!"
    else:
        userId = userIdRows[0]

    # Query keys table to retrieve first half of priv key, pub key, signature
    mycursor.execute("SELECT privKey, pubKey, signature FROM `keys` WHERE platform = %s AND userId = %s", (platform, userId))
    keyRows = mycursor.fetchone()
    if keyRows is None:
        return False, "Keys not found!"
    else:
        privKey1 = keyRows[0]
        pubKey = keyRows[1]
        signature = keyRows[2]

    # Construct path and read 2nd half of the private key
    usbFileName = os.path.join(usbDir, f"{username}Priv{platform}2.PEM")
    with open(usbFileName, 'rb') as file:
        privKey2 = file.read()

    # Combine them, load both private and public key object
    combinedPrivKey = privKey1 + privKey2
    privKey = rsa.PrivateKey.load_pkcs1(combinedPrivKey)

    # Retrieve img BLOB from DB
    mycursor.execute("SELECT photo FROM Images WHERE userId = %s AND platform = %s", (userId, platform))
    imgRows = mycursor.fetchone()

    if imgRows is None:
        return False, "Image not found!"
    else:
        img = imgRows[0]

    # Write img BLOB to a file
    tempImgFile = "tempImg.jpg"
    with open(tempImgFile, 'wb') as file:
        file.write(img)

    # Prompt users for passphrase
    passphrase = tkinter.simpledialog.askstring(title="Passphrase", prompt="Enter passphrase:", show='*')

    success, message, decPasswd = extract(platform, passphrase, privKey, tempImgFile, signature, pubKey)

    if success:
        return True, message, decPasswd
    else:
        return False, message
