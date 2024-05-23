#! /usr/bin/env python3
from utils.enc import enc
from utils.dec import dec
from utils.ver import ver
from utils.hide import hid


def main():
    print("""
Options
1. Generate
2. Decrypt
3. Verify
4. Hide
5. Quit\n
""")
    prompt = input("What do you want to do? ")

    if prompt == "1":
        platform = input("Platform: ")
        enc(platform)
    elif prompt == "2":
        platform = input("Platform: ")
        dec(platform)
    elif prompt == "3":
        platform = input("Platform: ")
        ver(platform)
    elif prompt == "4":
        hid()
    elif prompt == "5":
        print("Goodbye!")
        quit()
    else:
        print("\nInvalid option. Pick again!\n")
        main()


if __name__ == "__main__":
    main()
