def deleteImage(id, conn, mycursor, userId):
    mycursor.execute("SELECT userId, photo FROM Users WHERE username = %s AND photoId = %s", (userId, id))

    row = mycursor.fetchone()
    if row is None:
        print("Image does not exist!")
    else:
        mycursor.execute("DELETE FROM Images WHERE userId = %s", (userId,))
        conn.commit()
        print(f"Succefully removed {userId}'s account!")
