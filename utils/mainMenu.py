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

def prompt(frames):
    usernameT = tk.Label(frames, text="Username")
    usernameT.grid(row=0)

    passwordT = tk.Label(frames, text="Password")
    passwordT.grid(row=1)

    usernameTb = Entry(frames)
    usernameTb.grid(row=0, column=1)

    passwdTb = Entry(frames, show='*')
    passwdTb.grid(row=1, column=1)

    return usernameTb, passwdTb

def returnMain(curFrame, mainFrame):
    curFrame.destroy()
    mainFrame.pack()

def login(window, frame1):
    frame1.pack_forget()
    frame2 = Frame(window)
    frame2.pack()

    usernameTb, passwdTb = prompt(frame2)

    def handleLogin():
        username = usernameTb.get().encode('utf-8')
        passwd = passwdTb.get().encode('utf-8')
        loginAccount(username, passwd, conn, mycursor)
        
    submitButton = tk.Button(frame2, 
                        text="Login",
                        command=handleLogin)
    submitButton.grid(row=2, column=1)

    returnButton = tk.Button(frame2,
                             text="Cancel",
                             command=lambda: returnMain(frame2, frame1))
    returnButton.grid(row=2, column=0)

def create(window, frame1):
    frame1.pack_forget()
    frame3 = Frame(window)
    frame3.pack()

    usernameTb, passwdTb = prompt(frame3)

    def handleCreate():
        username = usernameTb.get().encode('utf-8')
        passwd = passwdTb.get().encode('utf-8')
        success = createAccount(username, passwd, conn, mycursor)
        user = username.decode()

        if success:
            successT = tk.Label(frame3, text=f"Account {user} created!")
            successT.grid(row=3, column=0, columnspan=2)
        else:
            failT = tk.Label(frame3, text=f"Account {user} not created!")
            failT.grid(row=3, column=0, columnspan=2)
        
    submitButton = tk.Button(frame3, 
                             text="Sign Up",
                             command=handleCreate)
    submitButton.grid(row=2, column=1)

    returnButton = tk.Button(frame3,
                             text="Cancel",
                             command=lambda: returnMain(frame3, frame1))
    returnButton.grid(row=2, column=0)
    

def delete(window, frame1):
    frame1.pack_forget()
    frame4 = Frame(window)
    frame4.pack()

    usernameTb, passwdTb = prompt(frame4)

    def handleDelete():
        username = usernameTb.get().encode('utf-8')
        passwd = passwdTb.get().encode('utf-8')
        deleteAccount(username, passwd, conn, mycursor)
        
    submitButton = tk.Button(frame4, 
                             text="Delete",
                             command=handleDelete)
    submitButton.grid(row=2, column=1)

    returnButton = tk.Button(frame4,
                             text="Cancel",
                             command=lambda: returnMain(frame4, frame1))
    returnButton.grid(row=2, column=0)
