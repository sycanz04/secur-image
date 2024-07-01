from utils.ver import ver
from utils.enc import enc
from utils.ls import listImage
from utils.gen import genPass
from utils.hide import extract
from utils.delete import deleteImage


def menu(conn, mycursor, username):
    print("""
Options
1. Insert
2. Generate
3. Decrypt
4. Verify
5. List Images
6. Delete Image
7. Quit\n
""")
    prompt = input("What do you want to do? ")
    match prompt:
        case "1":
            platform = input("Platform: ")
            passwd = input("Passwd: ")
            enc(passwd, platform, conn, mycursor, username)
        case "2":
            platform = input("Platform: ")
            genPass(platform, conn, mycursor, username)
        case "3":
            platform = input("Platform: ")
            extract(platform, conn, mycursor, username)
        case  "4":
            platform = input("Platform: ")
            ver(platform)
        case "5":
            passwd = input("Passwd: ")
            listImage(passwd, conn, mycursor, username)
        case "6":
            platform = input("Platform: ")
            deleteImage(platform, conn, mycursor, username)
        case "7":
            print("Goodbye!")
            quit()
        case _:
            print("\nInvalid option. Pick again!\n")
            exit()
