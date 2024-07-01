def listImage(conn, mycursor, username):
    mycursor.execute("SELECT I.photoId, I.platform FROM Images I JOIN Users U ON I.userId = U.userId WHERE U.username = %s", (username, ));

    row = mycursor.fetchone()
    if row is None:
        print("User does not have any images!")
    else:
        photoId = row[0]
        platform = row[1]

        print("Photo ID: ", photoId)
        print("Platform: ", platform)
    conn.commit()
