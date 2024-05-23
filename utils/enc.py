import rsa
import os
from utils.gen import genPass
from utils.hide import hidden
from dotenv import load_dotenv

# Load env var from .env files
load_dotenv()


# Define paths
baseDir = os.path.expanduser(os.getenv('BASE_DIR', '~/hello'))
pubDir = os.path.join(baseDir, "keys/pub")
privDir = os.path.join(baseDir, "keys/priv")
encpassDir = os.path.join(baseDir, "gamePrice")
signDir = os.path.join(baseDir, "sign")


def enc(name):
    pubPath = os.path.join(pubDir, f"pub{name}.pem")
    privPath = os.path.join(privDir, f"priv{name}.pem")
    encpassPath = os.path.join(encpassDir, f"{name}.txt")
    signPath = os.path.join(signDir, f"{name}Signature.txt")

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

    # Generates passwords
    passw = genPass()
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

    cont = input("Do you want to hide it in an image?(y/n) ")

    if cont == "y":
        cfName = input("Cover file format: ")
        efName = input("Embed file format: ")
        hidden(cfName, efName)
    elif cont == "n":
        print("See you again!")
        exit()
