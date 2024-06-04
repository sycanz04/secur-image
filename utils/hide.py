import os
from dotenv import load_dotenv

# Load env var from .env files
load_dotenv()


baseDir = os.path.expanduser(os.getenv('BASE_DIR', '~/hello'))
cf = os.path.expanduser('~/img')
ef = os.path.join(baseDir, 'gamePrice')


def hidden(platform, cFile, conn, mycursor, username):
    cfPath = os.path.join(cf, cFile)
    efPath = os.path.join(ef, f"{platform}.txt")

    if os.path.exists(cfPath):
        if os.path.exists(efPath):
            embedCommand = f"steghide embed -cf {cfPath} -ef {efPath}"
            os.system(embedCommand)
            print(f"{platform}.txt successfully embedded in {cFile}...\n")
            with open(cfPath, "rb") as file:
                binData = file.read()

            mycursor.execute("SELECT userId FROM Users WHERE username = %s", (username, ))
            row = mycursor.fetchone()
            if row is None:
                print("User does not exist!")
            else:
                userId = row[0]
                mycursor.execute("INSERT INTO Images(platform, photo, userId) VALUES (%s, %s, %s)", (platform, binData, userId))
            conn.commit()
            print("Stored in database!")

        else:
            print(f"{efPath} DNE!")
    else:
        print(f"{cfPath} DNE!")


def extract(platform, conn, mycursor, username):
    cfPath = os.path.join(baseDir, platform)

    sql = "SELECT username, photo FROM Images WHERE username = %s"
    mycursor.execute(sql, (platform, ))
    result = mycursor.fetchone()[1]

    storeFilePath = os.path.join(cf, f"{platform}.jpg")
    if os.path.exists(storeFilePath):
        with open(storeFilePath, 'wb') as file:
            file.write(result)
            file.close()
    else:
        with open(storeFilePath, 'wb') as file:
            file.write(result)
            file.close()

    # if os.path.exists(cfPath):
    #     embedCommand = f"steghide extract -sf {cfPath}"
    #     os.system(embedCommand)
    # else:
    #     print(f"{cfPath} DNE!")


def hid(conn, mycursor, userId):
    print("1. Embed ")
    print("2. Extract")
    option = input("Option: ")

    if option == "1":
        cfName = input("Cover file format: ")
        efName = input("Embed file format: ")
        hidden(cfName, efName, conn, mycursor, userId)

    elif option == "2":
        cfName = input("Cover file format: ")
        extract(cfName)
