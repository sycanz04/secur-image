def listImage(conn, mycursor, username):
    mycursor.execute("""SELECT I.photoId, I.platform
                      FROM Images I
                      JOIN Users U ON I.userId = U.userId
                      WHERE U.username = %s""", (username, ));

    row = mycursor.fetchall()
    if not rows:
        return False, "User does not have any images!"
    else:
        for row in rows:
            img = []
            imgId = row[0]
            platform = row[1]
            img.append((imgId, platform))

            return True, img

    conn.commit()
