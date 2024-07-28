#! /usr/bin/env python3

import traceback
import tkinter as tk
from tkinter import *
from logConfig import getLogger
from utils.mainMenu import login, create, delete

# Init logger
logger = getLogger(__name__)

# Init window elements
window = tk.Tk()
window.title("Secur Image")
window.geometry('800x500')
frame1 = Frame(window)
frame1.pack()

# Button helper function
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

# Main function displaying widgets
def main():
    logger.info("Program stars")
    try:
        projectT = tk.Label(frame1, text="Secur Image", font=('Arial', 30), pady=20)
        projectT.pack()
        menuT = tk.Label(frame1, text="Select an option", font=('Arial', 20), pady=15)
        menuT.pack()

        butt1 = createButt(frame1, "Login", lambda: login(window, frame1)).pack()
        butt2 = createButt(frame1, "Signup", lambda: create(window, frame1)).pack()
        butt3 = createButt(frame1, "Delete", lambda: delete(window, frame1)).pack()
        butt4 = createButt(frame1, "Quit", lambda: quitFunction(window)).pack()

        window.mainloop()

    except:
        logger.error("An error occured")
        print(traceback.format_exc())

main()
