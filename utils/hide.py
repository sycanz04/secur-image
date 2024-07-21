import os
from utils.dec import dec


def hidden(platform, cfFile, efFile, conn, mycursor, username, passphrase):
    if not os.path.exists(efFile):
        return False, f"*{efFile} DNE!*"

    # Embed encrypted password file into the image file
    embedCommand = f"steghide embed -cf {cfFile} -ef {efFile} -p {passphrase}"
    result = os.system(embedCommand)

    if result != 0:
        return False, "Failed to embed the file with steghide"

    # Read binary of image file
    with open(cfFile, "rb") as file:
        binData = file.read()

    # Insert it into the database
    mycursor.execute("SELECT userId FROM Users WHERE username = %s", (username, ))
    row = mycursor.fetchone()

    if row is None:
        return False, "*User does not exist!*"

    userId = row[0]
    mycursor.execute("INSERT INTO Images(platform, photo, userId) VALUES (%s, %s, %s)", (platform, binData, userId))
    os.remove(efFile)

    conn.commit()
    return True, "Operation successful!"

def extract(platform, conn, mycursor, username):
    mycursor.execute("Select userId from Users WHERE username = %s", (username,))
    userIdResult = mycursor.fetchone()

    if userIdResult:
        userId = userIdResult[0]
    else:
        raise ValueError("User not found")

    mycursor.execute("""SELECT Images.photo
                     FROM Images
                     INNER JOIN Users ON Images.userId = Users.userId
                     WHERE Images.platform = %s AND Users.userId = %s""", (platform, userId))
    imageResult = mycursor.fetchone()
    if userIdResult:
        image = imageResult[0]
    else:
        raise ValueError("Image not found")
    conn.commit()

    storeFilePath = os.path.join(cf, f"{username}{platform}.jpg")
    if os.path.exists(storeFilePath):
        with open(storeFilePath, 'wb') as file:
            file.write(image)
            file.close()
    else:
        with open(storeFilePath, 'wb') as file:
            file.write(image)
            file.close()

    if os.path.exists(storeFilePath):
        embedCommand = f"steghide extract -sf {storeFilePath}"
        os.system(embedCommand)
        dec(platform)
    else:
        print(f"{storeFilePath} DNE!")
