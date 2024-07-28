import rsa
import os
import traceback
import tkinter.simpledialog
from utils.hide import hidden
from logConfig import getLogger


# Init logger
logger = getLogger(__name__)

def enc(platform, passwd, imgFile, usbDir, conn, mycursor, username):
    logger.info("enc function called")
    try:
        # Generate 2048 bit pub and priv keys
        (pubKey, privKey) = rsa.newkeys(2048)
        loadedPubKey = pubKey.save_pkcs1()
        logger.info("Generated public and private key. Loaded public key object")

        # Generate path and split private key
        usbFilePath = os.path.join(usbDir, f"{username}Priv{platform}2.PEM")
        fullPrivKey = privKey.save_pkcs1()
        halfLenPrivKey = len(fullPrivKey) // 2
        privKey1 = fullPrivKey[:halfLenPrivKey]
        privKey2 = fullPrivKey[halfLenPrivKey:]
        logger.info("Split private keys into half length and ")

        # Store privKey2 in USB drive
        with open(usbFilePath, 'wb') as file:
            file.write(privKey2)
        logger.info("Wrote second half of private keys into usb drive")

        # Encrypting messages with pub key
        encryptedMessage = rsa.encrypt(passwd.encode(), pubKey)
        logger.info("Encrypted message with public key")

        # Initialise encPassFile to store it temporarily
        encPassFile = f"{platform}.txt"
        with open(encPassFile, 'wb') as file:
            file.write(encryptedMessage)
        logger.info("Wrote encrypted passwords into a file temporarily")

        # Generating signature
        signature = rsa.sign(encryptedMessage, privKey, "SHA-256")
        logger.info("Signed encrypted passwords")



        try:
            # Query userId
            mycursor.execute("SELECT userId FROM Users WHERE username = %s", (username,))
            logger.info("Fetched user id from database")
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
            logger.info("Values written into database")

            # Prompt users for passphrase
            passphrase = tkinter.simpledialog.askstring(title="Passphrase", prompt="Enter passphrase:", show='*')
            logger.info("Prompting user for passphrase")

            success, message = hidden(platform, imgFile, encPassFile, conn, mycursor, username, passphrase)
            if success:
                return True, message
            else:
                return False, message

        except Exception as err:
            conn.rollback()
            return False, f"Error: {err}"
    except:
        logger.error("An eror occured in enc function")
        print(traceback.format_exc())
