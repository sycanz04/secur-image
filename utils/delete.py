import bcrypt
import pyotp
import traceback
from logConfig import getLogger


# Init logger
logger = getLogger(__name__)

def deleteImage(passwd, conn, mycursor, username):
    logger.info("deleteImage function called")
    try:
        mycursor.execute("SELECT passwdHash, secretKey FROM Users WHERE username = %s", (username, ))
        logger.info("Fetched hashed password, secret key from database")
        row = mycursor.fetchone()

        if row is None:
            return False, "User does not exist!"
        else:
            hashedPasswd = row[0]
            secretKey = row[1]

            totp = pyotp.TOTP(secretKey)
            logger.info("TOTP object created")

            if bcrypt.checkpw(passwd, hashedPasswd.encode('utf-8')):
                logger.info("Password matched, proceeding.")
                otpPrompt = input("Enter OTP code: ")

                if totp.verify(otpPrompt):
                    logger.info("Valid OTP, proceeding.")
                    mycursor.execute("SELECT userId, photo FROM Users WHERE username = %s AND photoId = %s", (username, id))
                    logger.info("Fetched user id from database")
                    row = mycursor.fetchone()

                    if row is None:
                        return False, "Image does not exist!"
                    else:
                        mycursor.execute("DELETE FROM Images WHERE userId = (SELECT userId FROM Users WHERE username = %s", (username, ))
                        conn.commit()
                        logger.info("Account removed successfully")
                        return True, f"Succefully removed {username}'s account!"
                else:
                    logger.error("Invalid OTP")
                    return False, "Invalid OTP. Please try again."
            else:
                logger.error("Incorrect username or password")
                return False, "Incorrect username or password"
    except:
        logger.error("An error occured in deleteImage function")
        print(traceback.format_exc())
