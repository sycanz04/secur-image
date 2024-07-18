#! /usr/bin/env python3
from utils.account import loginAccount, createAccount, deleteAccount
import cred
import mysql.connector
from mysql.connector import Error
from tkinter import *
import tkinter as tk


try:
    conn = mysql.connector.connect(
        host=cred.hostname,
        user=cred.username,
        passwd=cred.passwd,
    )

    if conn.is_connected():
        mycursor = conn.cursor()
        # Create database if not exist
        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {cred.database};")
        # print(f"Database '{cred.database}' created or already existed.")

        # Use the newly created database
        mycursor.execute(f"USE {cred.database};")
        # print(f"Using database '{cred.database}'.")

except Error as e:
    print(f"Error: {e}")
    quit()

mycursor.execute("""CREATE TABLE IF NOT EXISTS Users
                    (userId int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                     username VARCHAR(50) NOT NULL,
                     passwdHash VARCHAR(255) NOT NULL,
                     secretKey VARCHAR(255) NOT NULL);""")
mycursor.execute("""CREATE TABLE IF NOT EXISTS Images
                    (photoId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                     platform VARCHAR(50) NOT NULL,
                     photo LONGBLOB NOT NULL,
                     userId INT NOT NULL,
                     FOREIGN KEY(userId) REFERENCES Users(userId));""")

window = tk.Tk()
window.title("Secur Image")
frame1 = Frame(window)

def prompt():
    frame1.destroy()
    frame2 = Frame(window)
    frame2.pack()

    usernameT = tk.Label(frame2, text="Username")
    usernameT.grid(row=0)
    
    passwordT = tk.Label(frame2, text="Password")
    passwordT.grid(row=1)

    usernameTb = Entry(frame2)
    usernameTb.grid(row=0, column=1)

    passwdTb = Entry(frame2, show='*')
    passwdTb.grid(row=1, column=1)

    def handleLogin():
        username = usernameTb.get()
        passwd = passwdTb.get()
        loginAccount(username, passwd, conn, mycursor)
        

    submitButton = tk.Button(frame2, 
                        text="Login",
                        command=handleLogin)
    submitButton.grid(row=2, column=0, columnspan=2)

def main():
    menuText = "Select an option"
    menu = tk.Label(frame1, text=menuText)
    menu.pack()

    button1 = tk.Button(frame1, 
                        text="Login",
                        command=prompt,
                        activebackground="blue", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="lightgray",
                        cursor="hand2",
                        disabledforeground="gray",
                        fg="black",
                        font=("Arial", 12),
                        height=2,
                        highlightbackground="black",
                        highlightcolor="green",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100)
    button1.pack()
    button2 = tk.Button(frame1, 
                        text="Signup", 
                        activebackground="blue", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="lightgray",
                        cursor="hand2",
                        disabledforeground="gray",
                        fg="black",
                        font=("Arial", 12),
                        height=2,
                        highlightbackground="black",
                        highlightcolor="green",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100)
    button2.pack()
    button3 = tk.Button(frame1, 
                        text="Delete", 
                        activebackground="blue", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="lightgray",
                        cursor="hand2",
                        disabledforeground="gray",
                        fg="black",
                        font=("Arial", 12),
                        height=2,
                        highlightbackground="black",
                        highlightcolor="green",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100)
    button3.pack()
    button4 = tk.Button(frame1, 
                        text="Quit", 
                        command=window.destroy,
                        activebackground="blue", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="lightgray",
                        cursor="hand2",
                        disabledforeground="gray",
                        fg="black",
                        font=("Arial", 12),
                        height=2,
                        highlightbackground="black",
                        highlightcolor="green",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100)
    button4.pack()

frame1.pack()
main()

window.mainloop()

    # prompt = input("What do you want to do? ")

    # if prompt == "1":
    #     username = input("Username: ")
    #     passwd = input("Password: ").encode('utf-8')
    #     loginAccount(username, passwd, conn, mycursor)
    # elif prompt == "2":
    #     username = input("Username: ")
    #     passwd = input("Password: ").encode('utf-8')
    #     createAccount(username, passwd, conn, mycursor)
    # elif prompt == "3":
    #     username = input("Username: ")
    #     passwd = input("Password: ").encode('utf-8')
    #     deleteAccount(username, passwd, conn, mycursor)
    # elif prompt == "4":
    #     print("Goodbye!")
    #     quit()
    # else:
    #     print("\nInvalid option. Pick again!\n")
    #     main()
