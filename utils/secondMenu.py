import os
import pyotp
import clipboard
import traceback
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from utils.enc import enc
from utils.dec import dec
from utils.gen import genPass
from logConfig import getLogger


# Init logger
logger = getLogger(__name__)

################## Helper Functions ##################

# Prompts user for platform name
def prompt(frames):
    logger.info("prompt function called")
    try:
        platformT = tk.Label(frames, text="Platform", font=('Arial', 20))
        platformT.grid(row=0, column=0)

        platformTb = Entry(frames)
        platformTb.grid(row=0, column=1)

        logger.info("Asked for platform name")
        return platformTb
    except:
        logger.error("An error occured in prompt function")
        print(traceback.format_exc())

# Prompts user for passwd
def getPasswd(frames):
    logger.info("getPasswd function called")
    try:
        passwdT = tk.Label(frames, text="Password", font=('Arial', 20))
        passwdT.grid(row=1, column=0)

        passwdTb = Entry(frames, show='*')
        passwdTb.grid(row=1, column=1)

        logger.info("Asked for password")
        return passwdTb
    except:
        logger.error("An error occured in getPasswd function")
        print(traceback.format_exc())

# Return to previous frame
def returnMain(curFrame, mainFrame):
    logger.info("returnMain function called")
    try:
        curFrame.destroy()
        mainFrame.pack()
        logger.info("Returned to previous frame")
    except:
        logger.error("An error occured in returnMain function")
        print(traceback.format_exc())

# Choose image file
def chooseImgPath(fileLabel):
    logger.info("chooseImgPath function called")
    try:
        filePath = filedialog.askopenfilename(initialdir='/home', title='Select an image')
        if filePath:
            fileLabel.config(text=filePath)
            logger.info("Image selected")
    except:
        logger.error("An error occured in choseImgPath function")
        print(traceback.format_exc())

# Choose usb dir
def chooseUsbDir(dirLabel):
    logger.info("chooseUsbDir function called")
    try:
        usbDir = filedialog.askdirectory(initialdir='/', title='Select USB location')
        if usbDir:
            dirLabel.config(text=usbDir)
    except:
        logger.error("An error occured in chooseUsbDir function")
        print(traceback.format_exc())

# Creates button
def createButton(frame, text, command):
    logger.info("createButton function called")
    try:
        newButton = tk.Button(frame, text=text, command=command)
        newButton.pack()
    except:
        logger.error("An error occured in createButton function")
        print(traceback.format_exc())

############# End of Helper Functions ###############

################## Main Functions ##################

def insert(window, frame5, conn, mycursor, username):
    logger.info("insert function called")
    try:
        frame5.pack_forget()
        frame7 = tk.Frame(window)
        frame7.pack()

        # Get platform name and passwd
        platform = prompt(frame7)
        passwd = getPasswd(frame7)

        imgFileLabel = tk.Label(frame7, text="No file selected")
        imgFileLabel.grid(row=2, column=0)
        imgFileButt = tk.Button(frame7, text="Choose Image file",
                             command=lambda: chooseImgPath(imgFileLabel))
        imgFileButt.grid(row=2, column=1)

        usbDirLabel = tk.Label(frame7, text="No dir selected")
        usbDirLabel.grid(row=3, column=0)
        usbDirButt = tk.Button(frame7, text="Choose USB dir",
                             command=lambda: chooseUsbDir(usbDirLabel))
        usbDirButt.grid(row=3, column=1)

        def handleInsert():
            logger.info("handleInsert function called")
            userPlatform = platform.get()
            userPasswd = passwd.get()
            imgFile = imgFileLabel.cget("text")
            usbDir = usbDirLabel.cget("text")
            logger.info("Retrieved platform, password, image, usb dir")

            for widget in frame7.grid_slaves(row=5):
                widget.destroy()

            if not userPlatform or not userPasswd or "No file selected" in imgFile or "No dir selected" in usbDir:
                errorT = tk.Label(frame7, text="*All fields are required!*", fg='#ff0000')
                errorT.grid(row=5, column=0, columnspan=2)
                logger.error("Unfilled username or password or image fields")
                return

            # Checks if img file and Usb dir exist
            if not os.path.exists(imgFile):
                failT = tk.Label(frame7, text="The image DNE!", fg='#ff0000')
                failT.grid(row=5, column=0, columnspan=2)
                logger.error("Selected image does not exist")
                return

            if not os.path.exists(usbDir):
                failT = tk.Label(frame7, text="The USB dir DNE!", fg='#ff0000')
                failT.grid(row=5, column=0, columnspan=2)
                logger.error("Select USB dir does not exist")
                return

            # If condition met, start encryption and embedding file
            success, message = enc(userPlatform, userPasswd, imgFile, usbDir, conn, mycursor, username)

            if success:
                successT = tk.Label(frame7, text=message)
                successT.grid(row=5, column=0, columnspan=2)
            else:
                failT = tk.Label(frame7, text=message, fg='#ff0000')
                failT.grid(row=5, column=0, columnspan=2)

        cancelButton = tk.Button(frame7, text="Cancel", command=lambda: returnMain(frame7, frame5))
        cancelButton.grid(row=4, column=0)

        submitButton = tk.Button(frame7, text="Done", command=handleInsert)
        submitButton.grid(row=4, column=1)
    except:
        logger.error("An error occured in insert function")
        print(traceback.format_exc())

def generate(window, frame5, conn, mycursor, username):
    logger.info("generate function called")
    try:
        frame5.pack_forget()
        frame8 = tk.Frame(window)
        frame8.pack()

        platform = prompt(frame8)

        imgFileLabel = tk.Label(frame8, text="No file selected")
        imgFileLabel.grid(row=1, column=0)
        imgFileButt = tk.Button(frame8, text="Choose Image file",
                             command=lambda: chooseImgPath(imgFileLabel))
        imgFileButt.grid(row=1, column=1)

        usbDirLabel = tk.Label(frame8, text="No dir selected")
        usbDirLabel.grid(row=2, column=0)
        usbDirButt = tk.Button(frame8, text="Choose USB dir",
                             command=lambda: chooseUsbDir(usbDirLabel))
        usbDirButt.grid(row=2, column=1)

        def handleGen():
            userPlatform = platform.get()
            imgFile = imgFileLabel.cget("text")
            usbDir = usbDirLabel.cget("text")
            logger.info("Retrieved platform, image, usb dir")

            for widget in frame8.grid_slaves(row=4):
                widget.destroy()

            if not userPlatform or "No file selected" in imgFile or "No dir selected" in usbDir:
                errorT = tk.Label(frame8, text="*All fields are required!*", fg='#ff0000')
                errorT.grid(row=4, column=0, columnspan=2)
                logger.error("Unfilled platform or image or usb dir")
                return

            # Checks if img file and Usb dir exist
            if not os.path.exists(imgFile):
                failT = tk.Label(frame8, text="The image DNE!", fg='#ff0000')
                failT.grid(row=4, column=0, columnspan=2)
                logger.error("Select image does not exist")
                return

            if not os.path.exists(usbDir):
                failT = tk.Label(frame8, text="The USB dir DNE!", fg='#ff0000')
                failT.grid(row=4, column=0, columnspan=2)
                logger.error("Select usb dir does not exist")
                return

            # If condition met, start encryption and embedding file
            success, message = genPass(userPlatform, imgFile, usbDir, conn, mycursor, username)

            if success:
                successT = tk.Label(frame8, text=message)
                successT.grid(row=4, column=0, columnspan=2)
            else:
                failT = tk.Label(frame8, text=message, fg='#ff0000')
                failT.grid(row=4, column=0, columnspan=2)

        cancelButton = tk.Button(frame8, text="Cancel", command=lambda: returnMain(frame8, frame5))
        cancelButton.grid(row=3, column=0)

        submitButton = tk.Button(frame8, text="Done", command=handleGen)
        submitButton.grid(row=3, column=1)
    except:
        logger.error("An error occured in generate function")
        print(traceback.format_exc())

def list(curFrame, frame5, mycursor, username, buttFunction):
    logger.info("list function called")
    try:
        userT = tk.Label(curFrame, text=username)
        userT.pack(padx=10, pady=10)

        def handleListImage():
            logger.info("handleListImage function called")
            mycursor.execute("""SELECT i.photoId, i.platform
                                FROM Images i
                                JOIN Users u ON i.userId = u.userId
                                WHERE u.username = %s""", (username, ))
            logger.info("Fetched photo id, platform from database")
            rows = mycursor.fetchall()

            if not rows:
                logger.error("Not matching password in database")
                return False, "No password stored!"
            else:
                img = []
                for results in rows:
                    photoId = results[0]
                    platform = results[1]
                    img.append((photoId, platform))

                return True, img

        success, result = handleListImage()
        if success:
            for imgId, platform in result:
                text = f"{imgId}: {platform}"
                createButton(curFrame, text, lambda : buttFunction(platform))
        else:
            errorLabel = tk.Label(curFrame, text=result, fg='#ff0000')
            errorLabel.pack()

        returnButton = tk.Button(curFrame, text='Thanks!', command=lambda: returnMain(curFrame, frame5))
        returnButton.pack()
    except:
        logger.error("An error occured in list function")
        print(traceback.format_exc())

def decrypt(window, frame5, mycursor, username):
    logger.info("decrypt function called")
    try:
        frame5.pack_forget()
        frame9 = tk.Frame(window)
        frame9.pack()

        def buttFunction(platform):
            logger.info("buttFunction called")
            frame9.pack_forget()
            pathFrame = tk.Frame(window)
            pathFrame.pack()

            platformT = tk.Label(pathFrame, text=f"Platform: {platform}")
            platformT.grid(row=0, columnspan=2)

            usbDirLabel = tk.Label(pathFrame, text="No dir selected")
            usbDirLabel.grid(row=1, column=0)
            usbDirButt = tk.Button(pathFrame, text="Choose USB dir", command=lambda: chooseUsbDir(usbDirLabel))
            usbDirButt.grid(row=1, column=1)

            def handleDec():
                logger.info("handDec function called")
                userPlatform = platform
                usbDir = usbDirLabel.cget("text")
                logger.info("Retrieved platform, usb dir")

                for widget in pathFrame.grid_slaves(row=3):
                    widget.destroy()

                if not userPlatform or "No dir selected" in usbDir:
                    errorT = tk.Label(pathFrame, text="*All fields are required!*", fg='#ff0000')
                    errorT.grid(row=3, column=0, columnspan=2)
                    logger.error("Unfilled platform or usb dir")
                    return

                if not os.path.exists(usbDir):
                    failT = tk.Label(pathFrame, text="The USB dir DNE!", fg='#ff0000')
                    failT.grid(row=3, column=0, columnspan=2)
                    logger.error("Selected USB dir does not exist")
                    return

                success, message, decPasswd = dec(userPlatform, usbDir, mycursor, username)

                if success:
                    logger.info("Decryption successful")
                    successT = tk.Label(pathFrame, text="Decryption successful!", fg='#0000ff')
                    successT.grid(row=3, column=0, columnspan=2)
                    successMB = messagebox.askyesno(title="Decrypt successful!", message=message)
                    if successMB:
                        clipboard.copy(decPasswd)
                        logger.info("Password copied to clipboard")
                    else:
                        return
                else:
                    failT = tk.Label(pathFrame, text=message, fg='#ff0000')
                    failT.grid(row=3, column=0, columnspan=2)

            cancelButton = tk.Button(pathFrame, text="Cancel", command=lambda: returnMain(pathFrame, frame9))
            cancelButton.grid(row=2, column=0)

            submitButton = tk.Button(pathFrame, text="Done", command=handleDec)
            submitButton.grid(row=2, column=1)

        list(frame9, frame5, mycursor, username, buttFunction)
    except:
        logger.error("An error occured in decrypt function")
        print(traceback.format_exc())


def delete(window, frame5, conn, mycursor, username):
    logger.info("delete function called")
    try:
        frame5.pack_forget()
        frame10 = tk.Frame(window)
        frame10.pack()

        def buttFunction(platform):
            logger.info("buttFunction called")
            frame10.pack_forget()
            otpFrame = tk.Frame(window)
            otpFrame.pack()

            mycursor.execute("SELECT secretKey FROM Users WHERE username = %s", (username, ))
            logger.info("Fetched secret key from database")
            row = mycursor.fetchone()

            if row:
                secretKey = row[0]
            else:
                tk.Label(frame10, text="*User not found!*", fg='#ff0000').pack()
                logger.error("Not matching user in database")
                otpFrame.destroy()
                return

            otpT = tk.Label(otpFrame, text="Enter the OTP on Google Authenticator to verify you're the owner")
            otpT.grid(row=0, columnspan=2)
            otpTb = tk.Entry(otpFrame, show='*')
            otpTb.grid(row=1, columnspan=2)

            def verifyOTP():
                logger.info("verifyOTP function called")
                otp = otpTb.get()
                totp = pyotp.TOTP(secretKey)

                if totp.verify(otp):
                    logger.info("Valid OTP, proceeding..")
                    mycursor.execute("""DELETE FROM Images
                                        WHERE userId = (SELECT userId FROM Users WHERE Username = %s)
                                        AND platform = %s""",
                                        (username, platform))
                    mycursor.execute("""DELETE FROM `keys`
                                        WHERE userId = (SELECT userId FROM Users WHERE Username = %s)
                                        AND platform = %s""",
                                        (username, platform))
                    conn.commit() 
                    logger.info("Deleted image and keys in database")

                    messagebox.showinfo(title="Delete Image Successful", message=f"Image {platform} deleted!")
                    returnMain(otpFrame, frame5)
                else:
                    logger.error("Invalid OTP")
                    failT = tk.Label(otpFrame, text="*Invalid OTP. Please try again.*", fg='#ff0000')
                    failT.grid(row=3, columnspan=2)
                    otpTb.delete(0, tk.END)

            # Return and submit button
            returnButt = Button(otpFrame, text='Return', command=lambda: returnMain(otpFrame, frame10))
            returnButt.grid(row=2, column=0)

            submitButt = Button(otpFrame, text='Submit', command=verifyOTP)
            submitButt.grid(row=2, column=1)

        list(frame10, frame5, mycursor, username, buttFunction)
    except:
        logger.error("An error occured in delete function")
        print(traceback.format_exc())

############### End of Main Functions ###############
