import rsa
import os
from dotenv import load_dotenv

# Load env var from .env files
load_dotenv()


baseDir = os.path.expanduser(os.getenv('BASE_DIR', '~/hello'))
pubDir = os.path.join(baseDir, "keys/pub")
privDir = os.path.join(baseDir, "keys/priv")
encpassDir = os.path.join(baseDir, "gamePrice")
signDir = os.path.join(baseDir, "sign")


def ver(platform):
    signPath = os.path.join(signDir, f"{platform}Signature.txt")
    pubPath = os.path.join(pubDir, f"pub{platform}.pem")
    encpassPath = os.path.join(encpassDir, f"{platform}.txt")

    if os.path.exists(signPath):
        with open(signPath, 'rb') as file:
            signature = file.read()
        with open(pubPath, 'rb') as file:
            pubKey = rsa.PublicKey.load_pkcs1(file.read())
        with open(encpassPath, 'rb') as file:
            msg = file.read()

        try:
            verified = rsa.verify(msg, signature, pubKey)
            print("Verfication: " + str(verified))
        except rsa.VerificationError:
            print("Verification failed: Signature does not match aka the file has been tampered with!")

    else:
        print("File does not exist!")
