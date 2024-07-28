import os
import rsa
import traceback
from logConfig import getLogger


# Init logger
logger = getLogger(__name__)

def hidden(platform, cfFile, efFile, conn, mycursor, username, passphrase):
    logger.info("hidden function called")
    try:
        if not os.path.exists(efFile):
            logger.error("efFile path DNE")
            return False, f"*{efFile} DNE!*"

        # Embed encrypted password file into the image file
        embedCommand = f"steghide embed -cf {cfFile} -ef {efFile} -p {passphrase}"
        result = os.system(embedCommand)
        logger.info("Encrypted password embedded into image")

        if result != 0:
            logger.error("Failed to embed file with steghide")
            return False, "Failed to embed the file with steghide"

        # Read binary of image file
        with open(cfFile, "rb") as file:
            binData = file.read()
        logger.info("Read image binary")

        # Insert it into the database
        mycursor.execute("SELECT userId FROM Users WHERE username = %s", (username, ))
        logger.info("Fetching user id from database")
        row = mycursor.fetchone()

        if row is None:
            logger.error("User does not exist")
            return False, "*User does not exist!*"

        userId = row[0]
        mycursor.execute("INSERT INTO Images(platform, photo, userId) VALUES (%s, %s, %s)", (platform, binData, userId))
        os.remove(efFile)
        logger.info("Values inserted to database and temporary efFile removed")

        conn.commit()
        logger.info("Operation successful")
        return True, "Operation successful!"

    except:
        logger.error("An error occured in hidden function")
        print(traceback.format_exc)

def extract(platform, passphrase, privKey, tempImgFile, signature, pubKey):
    try:
        # Extract file containing encPasswd
        embedCommand = f"steghide extract -sf {tempImgFile} -p {passphrase}"
        os.system(embedCommand)
        logger.info("Passphrase extracted from temporary image")

        extractedFilePath = f"{platform}.txt"
        if os.path.exists(extractedFilePath):
            # Read encPasswd
            with open(extractedFilePath, 'rb') as file:
                encPasswd = file.read()
            logger.info("Read efFile's binary")

            # Decrypt encPasswd into plaintext
            decPasswdByte = rsa.decrypt(encPasswd, privKey)
            decPasswd = decPasswdByte.decode()
            logger.info("Decrypted and decoded passwords with private key")

            # Remove temp files
            os.remove(tempImgFile)
            os.remove(extractedFilePath)
            logger.info("Removed temporary image and efFile")

            loadedPubKey = rsa.PublicKey.load_pkcs1(pubKey)
            try:
                verified = rsa.verify(encPasswd, signature, loadedPubKey)
                verification = f"Verification: {str(verified)}. Password is: {decPasswd}. Copy to clipboard?"
                logger.info("Password verification successful. All good")
                return True, verification, decPasswd
            except rsa.VerificationError:
                logger.error("Password verification failed. Password has been tampered!")
                return False, "Verification failed, file has been tampered!"

        else:
            return False, "Extraction failed"
    except:
        logger.error("An error occured in extract function")
        print(traceback.format_exc())
