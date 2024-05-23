import os
from dotenv import load_dotenv

# Load env var from .env files
load_dotenv()


baseDir = os.path.expanduser(os.getenv('BASE_DIR', '~/hello'))
cf = os.path.expanduser('~/img')
ef = os.path.join(baseDir, 'gamePrice')


def hidden(cFile, eFile):
    cfPath = os.path.join(cf, cFile)
    efPath = os.path.join(ef, f"{eFile}.txt")

    if os.path.exists(cfPath):
        if os.path.exists(efPath):
            embedCommand = f"steghide embed -cf {cfPath} -ef {efPath}"
            os.system(embedCommand)
            print(f"{eFile} successfully embedded in {cFile}")
        else:
            print(f"{efPath} DNE!")
    else:
        print(f"{cfPath} DNE!")


def extract(coverFile):
    cfPath = os.path.join(baseDir, coverFile)

    if os.path.exists(cfPath):
        embedCommand = f"steghide extract -sf {cfPath}"
        os.system(embedCommand)
    else:
        print(f"{cfPath} DNE!")


def hid():
    print("1. Embed ")
    print("2. Extract")
    option = input("Option: ")

    if option == "1":
        cfName = input("Cover file format: ")
        efName = input("Embed file format: ")

        hidden(cfName, efName)

    elif option == "2":
        cfName = input("Cover file format: ")
        extract(cfName)


if __name__ == "__main__":
    hid()
