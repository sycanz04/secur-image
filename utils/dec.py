import rsa
import os
from utils.ver import ver
from dotenv import load_dotenv

load_dotenv()

baseDir = os.path.expanduser(os.getenv('BASE_DIR', '~/hello'))
privDir = os.path.join(baseDir, 'keys/priv')
encpassDir = os.path.join(baseDir, 'gamePrice')


def dec(platform):
    try:
        privPath = os.path.join(privDir, f"priv{platform}.pem")
        encpassPath = os.path.join(encpassDir, f"{platform}.txt")

        # Retrieve priv key
        with open(privPath, "rb") as files:
            privKey = rsa.PrivateKey.load_pkcs1(files.read())

        # Retrieve enc key
        with open(encpassPath, "rb") as files:
            encPass = files.read()

        # Decode message
        clearMessage = rsa.decrypt(encPass, privKey)

        try:
            ver(platform)
            print("Clear message: " + clearMessage.decode())
        except Exception:
            print("Verification for signature failed!")

    except Exception as e:
        print(f"An error occured: {e}")
