import os
import rsa


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

def extract(platform, passphrase, privKey, tempImgFile, signature, pubKey):
    # Extract file containing encPasswd
    embedCommand = f"steghide extract -sf {tempImgFile} -p {passphrase}"
    os.system(embedCommand)

    extractedFilePath = f"{platform}.txt"
    if os.path.exists(extractedFilePath):
        # Read encPasswd
        with open(extractedFilePath, 'rb') as file:
            encPasswd = file.read()

        # Decrypt encPasswd into plaintext
        decPasswdByte = rsa.decrypt(encPasswd, privKey)
        decPasswd = decPasswdByte.decode()

        # Remove temp files
        os.remove(tempImgFile)
        os.remove(extractedFilePath)

        loadedPubKey = rsa.PublicKey.load_pkcs1(pubKey)
        try:
            verified = rsa.verify(encPasswd, signature, loadedPubKey)
            verification = f"Verification: {str(verified)}. Password is: {decPasswd}"
            return True, verification
        except rsa.VerificationError:
            return False, "Verification failed, file has been tampered with!"

        return True, decPasswd
    else:
        return False, "Extraction failed"
