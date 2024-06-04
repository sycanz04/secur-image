from utils.enc import enc
from utils.dec import dec
from utils.ver import ver
from utils.hide import extract
from utils.delete import deleteImage


def menu(conn, mycursor, username):
    print("""
Options
1. Generate
2. Decrypt
3. Verify
4. Delete Image
5. Quit\n
""")
    prompt = input("What do you want to do? ")

    if prompt == "1":
        platform = input("Platform: ")
        enc(platform, conn, mycursor, username)
    elif prompt == "2":
        platform = input("Platform: ")
        extract(platform, conn, mycursor, username)
    elif prompt == "3":
        platform = input("Platform: ")
        ver(platform)
    elif prompt == "4":
        id = input("Image ID: ")
        deleteImage(id, conn, mycursor, username)
    elif prompt == "5":
        print("Goodbye!")
        quit()
    else:
        print("\nInvalid option. Pick again!\n")
        exit()
