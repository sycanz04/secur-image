import rsa
import os
from utils.hide import hidden


# Define paths
baseDir = os.path.expanduser(os.getenv('BASE_DIR', '~/hello'))
pubDir = os.path.join(baseDir, "keys/pub")
privDir = os.path.join(baseDir, "keys/priv")
encpassDir = os.path.join(baseDir, "gamePrice")
signDir = os.path.join(baseDir, "sign")


def enc(passw, platform, conn, mycursor, username):
    pubPath = os.path.join(pubDir, f"pub{platform}.pem")
    privPath = os.path.join(privDir, f"priv{platform}.pem")
    encpassPath = os.path.join(encpassDir, f"{platform}.txt")
    signPath = os.path.join(signDir, f"{platform}Signature.txt")

    # Generate pub and priv keys
    (pubKey, privKey) = rsa.newkeys(1024)

    # Write pub and priv keys
    if os.path.exists(pubPath):
        with open(pubPath, 'wb') as file:
            file.write(pubKey.save_pkcs1("PEM"))
    else:
        with open(pubPath, 'wb') as file:
            file.write(pubKey.save_pkcs1("PEM"))

    if os.path.exists(privPath):
        with open(privPath, 'wb') as file:
            file.write(privKey.save_pkcs1("PEM"))
    else:
        with open(privPath, 'wb') as file:
            file.write(privKey.save_pkcs1("PEM"))

    # Encrypting messages with pub key
    encryptedMessage = rsa.encrypt(passw.encode(), pubKey)

    # Store passw in file
    if os.path.exists(encpassPath):
        with open(encpassPath, 'wb') as file:
            file.write(encryptedMessage)
    else:
        with open(encpassPath, 'wb') as file:
            file.write(encryptedMessage)

    # Generating signature
    if os.path.exists(signPath):
        signature = rsa.sign(encryptedMessage, privKey, "SHA-256")
        with open(signPath, 'wb') as file:
            file.write(signature)
    else:
        signature = rsa.sign(encryptedMessage, privKey, "SHA-256")
        with open(signPath, 'wb') as file:
            file.write(signature)

    cfName = input("Cover file format: ")
    hidden(platform, cfName, conn, mycursor, username)
