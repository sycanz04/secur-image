import string
import random
from utils.enc import enc


# Generates a 16 characters password
def genPass(platform, imgFile, usbDir, conn, mycursor, userId):
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
    print(f"finalPass: {finalPass}")

    success, message = enc(platform, finalPass, imgFile, usbDir, conn, mycursor, userId)
    if success:
        return True, message
    else:
        return False, message
