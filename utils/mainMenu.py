import os
import cred
import pyotp
import traceback
import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from mysql.connector import Error
from utils.second import menu
from logConfig import getLogger
from utils.account import loginAccount, createAccount, deleteAccount


# Init logger
logger = getLogger(__name__)

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

        # Use the newly created database
        mycursor.execute(f"USE {cred.database};")
        logger.info("Database connected and using specified database")

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
mycursor.execute("""CREATE TABLE IF NOT EXISTS `keys`
                    (keyId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    platform VARCHAR(255) NOT NULL,
                    pubKey BLOB NOT NULL,
                    privKey BLOB NOT NULL,
                    signature BLOB NOT NULL,
                    userId INT NOT NULL,
                    FOREIGN KEY(userId) REFERENCES Users(userId));""")

################ Helper Functions ################

def prompt(frames):
    logger.info("prompt function called")
    try:
        usernameT = tk.Label(frames, text="Username", font=('Arial', 15))
        usernameT.grid(row=0)

        passwordT = tk.Label(frames, text="Password", font=('Arial', 15))
        passwordT.grid(row=1)

        usernameTb = Entry(frames)
        usernameTb.grid(row=0, column=1)

        passwdTb = Entry(frames, show='*')
        passwdTb.grid(row=1, column=1)

        logger.info("Asked for username and passwords")
        return usernameTb, passwdTb
    except:
        logger.error("An error occured in prompt function")
        print(traceback.format_exc())

def returnMain(curFrame, mainFrame):
    logger.info("returnMain function called")
    try:
        curFrame.destroy()
        mainFrame.pack()
        logger.info("Returned to previous frame")
    except:
        logger.error("An occured in returnMain function")
        print(traceback.format_exc())

def cleaner(popup):
    logger.info("cleaner function called")
    try:
        popup.destroy()
        otpImgPath = 'totp.png'

        if os.path.exists(otpImgPath):
            os.remove(otpImgPath)
            logger.info("Temp OTP image removed")
        else:
            return False
    except:
        logger.error("An occured in cleaner function")
        print(traceback.format_exc())

############# End Helper Functions ##############

############### Main Function ###############

def login(window, frame1):
    logger.info("login function called")
    try:
        frame1.pack_forget()
        frame2 = Frame(window)
        frame2.pack()

        usernameTb, passwdTb = prompt(frame2)

        def handleLogin():
            logger.info("handleLogin function called")
            username = usernameTb.get()
            passwd = passwdTb.get().encode('utf-8')
            logger.info("Retrieved username and password")

            for widget in frame2.grid_slaves(row=3):
                widget.destroy()

            if not username or not passwd:
                errorT = tk.Label(frame2, text="*All fields are required!*", fg='#ff0000')
                errorT.grid(row=3, column=0, columnspan=2)
                logger.error("Unfilled username or password fields")
                return

            success, message = loginAccount(username, passwd, mycursor)

            if success:
                secretKey = message

                otpFrame = tk.Toplevel(frame2)
                otpFrame.title("Verify OTP")

                otpT = tk.Label(otpFrame, text="Enter the OTP on Google Authenticator to verify you're the owner")
                otpT.pack()
                otpTb = tk.Entry(otpFrame, show='*')
                otpTb.pack()
                logger.info("Prompted for OTP")

                def verifyOTP():
                    logger.info("verifyOTP function called, verifying OTP")
                    otp = otpTb.get()
                    totp = pyotp.TOTP(secretKey)
                    if totp.verify(otp):
                        logger.info("Valid OTP, proceeding..")
                        otpFrame.destroy()
                        menu(window, frame2, conn, mycursor, username)
                    else:
                        logger.error("Invalid OTP.")
                        failT = tk.Label(otpFrame, text="*Invalid OTP. Please try again.*", fg='#ff0000')
                        failT.pack()
                        otpTb.delete(0, tk.END)

                otpButt = Button(otpFrame, text='Submit', command=verifyOTP)
                otpButt.pack()

            else:
                failT = tk.Label(frame2, text=message, fg='#ff0000')
                failT.grid(row=3, column=0, columnspan=2)
                usernameTb.delete(0, tk.END)
                passwdTb.delete(0, tk.END)

        submitButton = tk.Button(frame2, text="Login", command=handleLogin)
        submitButton.grid(row=2, column=1)

        returnButton = tk.Button(frame2, text="Cancel", command=lambda: returnMain(frame2, frame1))
        returnButton.grid(row=2, column=0)
    except:
        logger.error("An error occured in login function")
        print(traceback.format_exc())

def create(window, frame1):
    logger.info("create function called")
    try:
        frame1.pack_forget()
        frame3 = Frame(window)
        frame3.pack()

        usernameTb, passwdTb = prompt(frame3)

        rePasswordT = tk.Label(frame3, text="Re-enter Password")
        rePasswordT.grid(row=2, column=0)
        rePasswdTb = Entry(frame3, show='*')
        rePasswdTb.grid(row=2, column=1)

        def handleCreate():
            logger.info("handleCreate function called")
            username = usernameTb.get()
            passwd = passwdTb.get().encode('utf-8')
            repasswd = rePasswdTb.get().encode('utf-8')
            logger.info("Retrieved username and passwords")
            
            for widget in frame3.grid_slaves(row=4):
                widget.destroy()

            if not username or not passwd or not repasswd:
                errorT = tk.Label(frame3, text="*All fields are required!*", fg='#ff0000')
                errorT.grid(row=4, column=0, columnspan=2)
                logger.error("Unfilled username or password fields")
                return

            if passwd == repasswd:
                logger.info("Passwords matched, proceeding..")
                success = createAccount(username, passwd, conn, mycursor)

                if success:
                    successT = tk.Label(frame3, text=f"Account {username} created!")
                    successT.grid(row=4, column=0, columnspan=2)

                    popup = Toplevel(frame3)
                    popup.title("OTP Setup")
                    logger.info("Setting up OTP")

                    setupT1 = Label(popup, text="To login into your account on SecurImage, you have to setup an OTP.")
                    setupT1.pack()
                    setupT2 = Label(popup, text="Scan below QR code with Google Authenticator app, DO NOT SHOW IT TO ANYONE!")
                    setupT2.pack()

                    # Display OTP image
                    img = tk.PhotoImage(file="totp.png")
                    imgLabel = tk.Label(popup, image=img)
                    imgLabel.image = img
                    imgLabel.pack()

                    doneButt = Button(popup, text="Done", command=lambda: cleaner(popup))
                    doneButt.pack()
                    logger.info("OTP setup done")
                else:
                    failT = tk.Label(frame3, text=f"*Account {username} not created!*", fg='#ff0000')
                    failT.grid(row=4, column=0, columnspan=2)
            else:
                mismatchT = tk.Label(frame3, text="*Passwords don't match!*", fg='#ff0000')
                mismatchT.grid(row=4, column=0, columnspan=2)
                logger.error("Passwords don't match")
                passwdTb.delete(0, tk.END)
                rePasswdTb.delete(0, tk.END)

        submitButton = tk.Button(frame3, text="Sign Up", command=handleCreate)
        submitButton.grid(row=3, column=1)

        returnButton = tk.Button(frame3, text="Cancel", command=lambda: returnMain(frame3, frame1))
        returnButton.grid(row=3, column=0)

    except:
        logger.info("An error occured in create function")
        print(traceback.format_exc())

def delete(window, frame1):
    logger.info("delete function called")
    try:
        frame1.pack_forget()
        frame4 = Frame(window)
        frame4.pack()

        usernameTb, passwdTb = prompt(frame4)

        def handleDelete():
            logger.info("handleDelete function called")
            username = usernameTb.get()
            passwd = passwdTb.get().encode('utf-8')
            logger.info("Retrieved username and password")

            for widget in frame4.grid_slaves(row=4):
                widget.destroy()

            if not username or not passwd:
                errorT = tk.Label(frame4, text="*All fields are required!*", fg='#ff0000')
                errorT.grid(row=4, column=0, columnspan=2)
                logger.error("Unfilled username or password fields")
                return

            # Re-confirm with user to delete account
            if messagebox.askyesno(title="Confirm Deletion", message=f"Are you sure you want to delete the account {username}?"):
                success, message = deleteAccount(username, passwd, conn, mycursor)
                if success:
                    successT = tk.Label(frame4, text=message)
                    successT.grid(row=4, column=0, columnspan=2)
                else:
                    failT = tk.Label(frame4, text=message, fg='#ff0000')
                    failT.grid(row=4, column=0, columnspan=2)
                    passwdTb.delete(0, tk.END)
            else:
                cancelT = tk.Label(frame4, text="Account deletion cancelled.", fg='#0000ff')
                cancelT.grid(row=4, column=0, columnspan=2)
                logger.info("Account deletion cancelled")

        submitButton = tk.Button(frame4, text="Delete", command=handleDelete)
        submitButton.grid(row=3, column=1)

        returnButton = tk.Button(frame4, text="Cancel", command=lambda: returnMain(frame4, frame1))
        returnButton.grid(row=3, column=0)

    except:
        logger.info("An error occured in delete function")
        print(traceback.format_exc())

############## End of main function ##############
