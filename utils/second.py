from utils.ver import ver
from utils.enc import enc
from utils.ls import listImage
from utils.gen import genPass
from utils.hide import extract
from utils.delete import deleteImage
from utils.secondMenu import insert, list
from tkinter import *
import tkinter as tk


def menu(window, frame2, conn, mycursor, username):
    frame2.pack_forget()
    frame5 = Frame(window)
    frame5.pack()
    welcomeT = tk.Label(frame5, text=f"Welcome, {username}!")
    welcomeT.pack()
    menuT = tk.Label(frame5, text="Select an option")
    menuT.pack()

    button1 = tk.Button(frame5, 
                        text="Insert",
                        command=lambda: insert(window, frame5, conn, mycursor, username),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button1.pack()
    button2 = tk.Button(frame5, 
                        text="Generate", command=lambda: login(window, frame5),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button2.pack()
    button3 = tk.Button(frame5, 
                        text="Decrypt", command=lambda: login(window, frame5),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button3.pack()
    button4 = tk.Button(frame5, 
                        text="Verify", command=lambda: login(window, frame5),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button4.pack()
    button5 = tk.Button(frame5, 
                        text="List Image",
                        command=lambda: list(window, frame5, conn, mycursor, username),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button5.pack()
    button6 = tk.Button(frame5, 
                        text="Delete Image", command=lambda: login(window, frame5),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button6.pack()
    button7 = tk.Button(frame5, 
                        text="Quit", command=window.destroy,
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button7.pack()

# def menu(conn, mycursor, username):
#     print("""
# Options
# 1. Insert
# 2. Generate
# 3. Decrypt
# 4. Verify
# 5. List Images
# 6. Delete Image
# 7. Quit\n
# """)
#     prompt = input("What do you want to do? ")
#     match prompt:
#         case "1":
#             platform = input("Platform: ")
#             passwd = input("Passwd: ")
#             enc(passwd, platform, conn, mycursor, username)
#         case "2":
#             platform = input("Platform: ")
#             genPass(platform, conn, mycursor, username)
#         case "3":
#             platform = input("Platform: ")
#             extract(platform, conn, mycursor, username)
#         case  "4":
#             platform = input("Platform: ")
#             ver(platform)
#         case "5":
#             listImage(conn, mycursor, username)
#         case "6":
#             platform = input("Platform: ")
#             deleteImage(platform, conn, mycursor, username)
#         case "7":
#             print("Goodbye!")
#             quit()
#         case _:
#             print("\nInvalid option. Pick again!\n")
#             exit()
