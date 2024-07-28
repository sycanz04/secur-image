import traceback
import tkinter as tk
from tkinter import *
from logConfig import getLogger
from utils.secondMenu import insert, generate, decrypt, delete

# Init logger
logger = getLogger(__name__)

def createButt(frame, text, command):
    return tk.Button(frame,
                     text=text, command=command,
                     activebackground="blue", activeforeground="white",
                     anchor="center", bd=3, bg="lightgray", cursor="hand2",
                     disabledforeground="gray", fg="black", font=("Arial", 15),
                     height=2, highlightbackground="black", highlightcolor="green",
                     highlightthickness=2, justify="center", overrelief="raised",
                     padx=10, pady=5, width=15, wraplength=150)

def quitFunction(window):
    logger.info("Program ends")
    window.destroy()

def menu(window, frame2, conn, mycursor, username):
    logger.info("menu function called")
    try:
        frame2.pack_forget()
        frame5 = Frame(window)
        frame5.pack()
        welcomeT = tk.Label(frame5, text=f"Welcome, {username}!", font=('Arial', 35), pady=20)
        welcomeT.pack()
        menuT = tk.Label(frame5, text="Select an option", font=('Arial', 25), pady=15)
        menuT.pack()

        butt1 = createButt(frame5, "Insert", lambda: insert(window, frame5, conn, mycursor, username)).pack()
        butt2 = createButt(frame5, "Generate", lambda: generate(window, frame5, conn, mycursor, username)).pack()
        butt3 = createButt(frame5, "Decrypt", lambda: decrypt(window, frame5, mycursor, username)).pack()
        butt4 = createButt(frame5, "Delete", lambda: delete(window, frame5, conn, mycursor, username)).pack()
        butt5 = createButt(frame5, "Quit", lambda: quitFunction(window)).pack()
    except:
        logger.error("An error occured in menu function")
        print(traceback.format_exc())
