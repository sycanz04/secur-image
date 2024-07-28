import string
import random
import traceback
from utils.enc import enc
from logConfig import getLogger


# Init logger
logger = getLogger(__name__)
# Generates a 16 characters password
def genPass(platform, imgFile, usbDir, conn, mycursor, userId):
    logger.info("genPass function called")
    try:
        asciiLower = string.ascii_lowercase
        asciiUpper = string.ascii_uppercase
        asciiNumbers = string.digits
        asciiPunc = string.punctuation
        passwordSec = 4

        sec1 = "".join(random.choice(asciiLower) for i in range(passwordSec))
        sec2 = "".join(random.choice(asciiUpper) for i in range(passwordSec))
        sec3 = "".join(random.choice(asciiNumbers) for i in range(passwordSec))
        sec4 = "".join(random.choice(asciiPunc) for i in range(passwordSec))

        combinedPass = sec1+sec2+sec3+sec4
        listPass = list(combinedPass)
        random.shuffle(listPass)
        finalPass = ''.join(listPass)
        logger.info("Random password generated")

        success, message = enc(platform, finalPass, imgFile, usbDir, conn, mycursor, userId)
        if success:
            return True, message
        else:
            return False, message
    except:
        logger.error("An error occured in genPass function")
        print(traceback.format_exc())
