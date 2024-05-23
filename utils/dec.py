import rsa
import os
from dotenv import load_dotenv

load_dotenv()

baseDir = os.path.expanduser(os.getenv('BASE_DIR', '~/hello'))
privDir = os.path.join(baseDir, 'keys/priv')
encpassDir = os.path.join(baseDir, 'gamePrice')


def dec(name):
    try:
        privPath = os.path.join(privDir, f"priv{name}.pem")
        encpassPath = os.path.join(encpassDir, f"{name}.txt")

        # Retrieve priv key
        with open(privPath, "rb") as files:
            privKey = rsa.PrivateKey.load_pkcs1(files.read())

        # Retrieve enc key
        with open(encpassPath, "rb") as files:
            encPass = files.read()

        # Decode message
        clearMessage = rsa.decrypt(encPass, privKey)

        print("Clear message: " + clearMessage.decode())
    except Exception as e:
        print(f"An error occured: {e}")
