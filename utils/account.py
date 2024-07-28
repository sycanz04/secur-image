import bcrypt
import pyotp
import qrcode
import traceback
from logConfig import getLogger


# Init logger
logger = getLogger(__name__)

def loginAccount(username, passwd, mycursor):
    logger.info("loginAccount function called")
    try:
        mycursor.execute("SELECT passwdHash, secretKey FROM Users WHERE username = %s", (username, ))
        logger.info("Fetched username, hashed password, secret key from database")

        row = mycursor.fetchone()
        if row is None:
            message = "*User does not exist!*"
            logger.error(message)
            return False, message
        else:
            hashedPasswd = row[0]
            secretKey = row[1]

            logger.info("Checking password")
            if bcrypt.checkpw(passwd, hashedPasswd.encode('utf-8')):
                # OTP will be validated in login function
                logger.info("Password match. Returning secret key")
                return True, secretKey
            else:
                message = "*Incorrect username or password!*"
                logger.error(message)
                return False, message
    except:
        logger.error("An error occured in loginAccount function")
        print(traceback.format_exc())


def createAccount(username, passwd, conn, mycursor):
    logger.info("createAccount function called")
    try:
        hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
        logger.info("Hashed password")
        secretKey = pyotp.random_base32()
        logger.info("Generated OTP secret key")

        uri = pyotp.totp.TOTP(secretKey).provisioning_uri(name=username, issuer_name="securImage")
        qrcode.make(uri).save("totp.png")
        logger.info("OTP URI generated and save in totp.png")

        mycursor.execute("INSERT INTO Users(username, passwdHash, secretKey) values (%s, %s, %s)", (username, hashed, secretKey))
        logger.info("Inserted username, hashed password, secretkey from database")
        conn.commit()
        return True
    except Exception as e:
        logger.error("*An error occured!*")
        return False, e

def deleteAccount(username, passwd, conn, mycursor):
    logger.info("deleteAccount function called")
    try:
        mycursor.execute("SELECT passwdHash FROM Users WHERE username = %s", (username,))
        logger.info("Fetched hashed password from database")
        row = mycursor.fetchone()

        if row is None:
            message = "*User does not exist!*"
            logger.error(message)
            return False, message
        else:
            hashedPasswd = row[0]
            if bcrypt.checkpw(passwd, hashedPasswd.encode('utf-8')):
                mycursor.execute("DELETE FROM Users WHERE username = %s", (username,))
                conn.commit()
                logger.info("Successfully removed account!")
                return True, f"Successfully removed {username}'s account!"
            else:
                message = "*Incorrect username or password*"
                logger.error(message)
                return False, message
    except Exception as e:
        logger.error("An error occured")
        return False, f"*Error deleting account: {e}*"
