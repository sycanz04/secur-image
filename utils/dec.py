import os
import rsa
import traceback
import tkinter.simpledialog
from utils.hide import extract
from logConfig import getLogger


# Init logger
logger = getLogger(__name__)
def dec(platform, usbDir, mycursor, username):
    logger.info("dec function called")
    try:
        # Query userId
        mycursor.execute("SELECT userId FROM Users WHERE username = %s", (username,))
        logger.info("Fetched user id from database")
        userIdRows = mycursor.fetchone()

        if userIdRows is None:
            return False, "User not found!"
        else:
            userId = userIdRows[0]

        # Query keys table to retrieve first half of priv key, pub key, signature
        mycursor.execute("SELECT privKey, pubKey, signature FROM `keys` WHERE platform = %s AND userId = %s", (platform, userId))
        logger.info("Fetched private key, public key, signature from database")
        keyRows = mycursor.fetchone()

        if keyRows is None:
            message = "Keys not found!"
            logger.error(message)
            return False, message
        else:
            privKey1 = keyRows[0]
            pubKey = keyRows[1]
            signature = keyRows[2]

        # Construct path and read 2nd half of the private key
        usbFileName = os.path.join(usbDir, f"{username}Priv{platform}2.PEM")
        with open(usbFileName, 'rb') as file:
            privKey2 = file.read()
        logger.info("Read second hald of private key from USB")

        # Combine them, load both private and public key object
        combinedPrivKey = privKey1 + privKey2
        privKey = rsa.PrivateKey.load_pkcs1(combinedPrivKey)
        logger.info("Combined both parts of private key and loaded as RSA object")

        # Retrieve img BLOB from DB
        mycursor.execute("SELECT photo FROM Images WHERE userId = %s AND platform = %s", (userId, platform))
        logger.info("Fetched image blob from database")
        imgRows = mycursor.fetchone()

        if imgRows is None:
            message = "*Image not found!*"
            logger.error(message)
            return False, message
        else:
            img = imgRows[0]

        # Write img BLOB to a file
        tempImgFile = "tempImg.jpg"
        with open(tempImgFile, 'wb') as file:
            file.write(img)
        logger.info("Image blob writte in database")

        # Prompt users for passphrase
        passphrase = tkinter.simpledialog.askstring(title="Passphrase", prompt="Enter passphrase:", show='*')

        success, message, decPasswd = extract(platform, passphrase, privKey, tempImgFile, signature, pubKey)

        if success:
            return True, message, decPasswd
        else:
            return False, message

    except:
        logger.exception("An unexpected error occured in dec function")
        print(traceback.format_exc())

