import os
import pyotp
from utils.enc import enc
from utils.dec import dec
from utils.gen import genPass
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox


################## Basic Functions ##################

# Prompts user for platform name
def prompt(frames):
    platformT = tk.Label(frames, text="Platform", font=('Arial', 20))
    platformT.grid(row=0, column=0)

    platformTb = Entry(frames)
    platformTb.grid(row=0, column=1)

    return platformTb

# Prompts user for passwd
def getPasswd(frames):
    passwdT = tk.Label(frames, text="Password", font=('Arial', 20))
    passwdT.grid(row=1, column=0)

    passwdTb = Entry(frames, show='*')
    passwdTb.grid(row=1, column=1)

    return passwdTb

# Return to previous frame
def returnMain(curFrame, mainFrame):
    curFrame.destroy()
    mainFrame.pack()

# Choose image file path
def chooseImgPath(fileLabel):
    filePath = filedialog.askopenfilename(initialdir='/home', title='Select an image')
    if filePath:
        fileLabel.config(text=filePath)

# Choose usb dir
def chooseUsbDir(dirLabel):
    usbDir = filedialog.askdirectory(initialdir='/', title='Select USB location')
    if usbDir:
        dirLabel.config(text=usbDir)

# Creates button
def createButton(frame, text, command):
    newButton = tk.Button(frame, text=text, command=command)
    newButton.pack()

############# End of Basic Functions ###############

################## Main Functions ##################

def insert(window, frame5, conn, mycursor, username):
    frame5.pack_forget()
    frame7 = tk.Frame(window)
    frame7.pack()

    # Get platform name and passwd
    platform = prompt(frame7)
    passwd = getPasswd(frame7)

    # Labels to display selected file
    imgFileLabel = tk.Label(frame7, text="No file selected")
    imgFileLabel.grid(row=2, column=0)

    # Choose an image
    imgFileButt = tk.Button(frame7, text="Choose Image file",
                         command=lambda: chooseImgPath(imgFileLabel))
    imgFileButt.grid(row=2, column=1)

    # Labels to display selected dir
    usbDirLabel = tk.Label(frame7, text="No dir selected")
    usbDirLabel.grid(row=3, column=0)

    # Choose a path
    usbDirButt = tk.Button(frame7, text="Choose USB dir",
                         command=lambda: chooseUsbDir(usbDirLabel))
    usbDirButt.grid(row=3, column=1)

    def handleInsert():
        userPlatform = platform.get()
        userPasswd = passwd.get()
        imgFile = imgFileLabel.cget("text")
        usbDir = usbDirLabel.cget("text")

        # Remove any existing error message
        for widget in frame7.grid_slaves(row=5):
            widget.destroy()

        # Checks if all required fields are filled
        if not userPlatform or not userPasswd or "No file selected" in imgFile:
            errorT = tk.Label(frame7, text="*All fields are required!*", fg='#ff0000')
            errorT.grid(row=5, column=0, columnspan=2)
            return

        # Checks if img file and Usb dir exist
        if not os.path.exists(imgFile):
            failT = tk.Label(frame7, text="The image DNE!", fg='#ff0000')
            failT.grid(row=5, column=0, columnspan=2)
            return

        if not os.path.exists(usbDir):
            failT = tk.Label(frame7, text="The USB dir DNE!", fg='#ff0000')
            failT.grid(row=5, column=0, columnspan=2)
            return

        # If condition met, start encryption and embedding file
        success, message = enc(userPlatform, userPasswd, imgFile, usbDir, conn, mycursor, username)

        if success:
            successT = tk.Label(frame7, text=message)
            successT.grid(row=5, column=0, columnspan=2)
        else:
            failT = tk.Label(frame7, text=message, fg='#ff0000')
            failT.grid(row=5, column=0, columnspan=2)

    cancelButton = tk.Button(frame7, text="Cancel",
                             command=lambda: returnMain(frame7, frame5))
    cancelButton.grid(row=4, column=0)

    submitButton = tk.Button(frame7, text="Done",
                             command=handleInsert)
    submitButton.grid(row=4, column=1)

def generate(window, frame5, conn, mycursor, username):
    # Things
    frame5.pack_forget()
    frame8 = tk.Frame(window)
    frame8.pack()

    # Get platform name
    platform = prompt(frame8)

    # Labels to display selected file
    imgFileLabel = tk.Label(frame8, text="No file selected")
    imgFileLabel.grid(row=1, column=0)

    # Choose an image
    imgFileButt = tk.Button(frame8, text="Choose Image file",
                         command=lambda: chooseImgPath(imgFileLabel))
    imgFileButt.grid(row=1, column=1)

    # Labels to display selected dir
    usbDirLabel = tk.Label(frame8, text="No dir selected")
    usbDirLabel.grid(row=2, column=0)

    # Choose a path
    usbDirButt = tk.Button(frame8, text="Choose USB dir",
                         command=lambda: chooseUsbDir(usbDirLabel))
    usbDirButt.grid(row=2, column=1)

    def handleGen():
        userPlatform = platform.get()
        imgFile = imgFileLabel.cget("text")
        usbDir = usbDirLabel.cget("text")

        # Remove any existing error message
        for widget in frame8.grid_slaves(row=4):
            widget.destroy()

        # Checks if all required fields are filled
        if not userPlatform or "No file selected" in imgFile:
            errorT = tk.Label(frame8, text="*All fields are required!*", fg='#ff0000')
            errorT.grid(row=4, column=0, columnspan=2)
            return

        # Checks if img file and Usb dir exist
        if not os.path.exists(imgFile):
            failT = tk.Label(frame8, text="The image DNE!", fg='#ff0000')
            failT.grid(row=4, column=0, columnspan=2)
            return

        if not os.path.exists(usbDir):
            failT = tk.Label(frame8, text="The USB dir DNE!", fg='#ff0000')
            failT.grid(row=4, column=0, columnspan=2)
            return

        # If condition met, start encryption and embedding file
        success, message = genPass(userPlatform, imgFile, usbDir, conn, mycursor, username)

        if success:
            successT = tk.Label(frame8, text=message)
            successT.grid(row=4, column=0, columnspan=2)
        else:
            failT = tk.Label(frame8, text=message, fg='#ff0000')
            failT.grid(row=4, column=0, columnspan=2)

    cancelButton = tk.Button(frame8, text="Cancel",
                             command=lambda: returnMain(frame8, frame5))
    cancelButton.grid(row=3, column=0)

    submitButton = tk.Button(frame8, text="Done",
                             command=handleGen)
    submitButton.grid(row=3, column=1)

def list(curFrame, frame5, mycursor, username, buttFunction):
    # Display username
    userT = tk.Label(curFrame, text=username)
    userT.pack(padx=10, pady=10)

    def handlelistImage():
        mycursor.execute("""SELECT i.photoId, i.platform
                            FROM Images i
                            JOIN Users u ON i.userId = u.userId
                            WHERE u.username = %s""", (username, ))
        rows = mycursor.fetchall()
        if not rows:
            return False, "No password stored!"
        else:
            img = []
            for results in rows:
                photoId = results[0]
                platform = results[1]
                img.append((photoId, platform))

            return True, img

    success, result = handlelistImage()
    if success:
        for imgId, platform in result:
            text = f"{imgId}: {platform}"
            createButton(curFrame, text, lambda : buttFunction(platform))
    else:
        errorLabel = tk.Label(curFrame, text=result, fg='#ff0000')
        errorLabel.pack()

    returnButton = tk.Button(curFrame, text='Thanks!',
                             command=lambda: returnMain(curFrame, frame5))
    returnButton.pack()

def decrypt(window, frame5, conn, mycursor, username):
    frame5.pack_forget()
    frame9 = tk.Frame(window)
    frame9.pack()

    def buttFunction(platform):
        # Frame to retrieve key paths
        frame9.pack_forget()
        pathFrame = tk.Frame(window)
        pathFrame.pack()

        # Display platform name
        platformT = tk.Label(pathFrame, text=f"Platform: {platform}")
        platformT.grid(row=0, columnspan=2)

        # Labels to display selected dir
        usbDirLabel = tk.Label(pathFrame, text="No dir selected")
        usbDirLabel.grid(row=1, column=0)

        # Buttons to select dir in USB
        usbDirButt = tk.Button(pathFrame, text="Choose USB dir",
                             command=lambda: chooseUsbDir(usbDirLabel))
        usbDirButt.grid(row=1, column=1)

        def handleDec():
            userPlatform = platform
            usbDir = usbDirLabel.cget("text")

            # Remove any existing error message
            for widget in pathFrame.grid_slaves(row=3):
                widget.destroy()

            # Checks if all required fields are filled
            if not userPlatform or "No dir selected" in usbDir:
                errorT = tk.Label(pathFrame, text="*All fields are required!*", fg='#ff0000')
                errorT.grid(row=3, column=0, columnspan=2)
                return

            if not os.path.exists(usbDir):
                failT = tk.Label(pathFrame, text="The USB dir DNE!", fg='#ff0000')
                failT.grid(row=3, column=0, columnspan=2)
                return

            success, message = dec(userPlatform, usbDir, mycursor, username)

            if success:
                successT = tk.Label(pathFrame, text=message)
                successT.grid(row=3, column=0, columnspan=2)
            else:
                failT = tk.Label(pathFrame, text=message, fg='#ff0000')
                failT.grid(row=3, column=0, columnspan=2)

        cancelButton = tk.Button(pathFrame, text="Cancel",
                                 command=lambda: returnMain(pathFrame, frame9))
        cancelButton.grid(row=2, column=0)

        submitButton = tk.Button(pathFrame, text="Done",
                                 command=handleDec)
        submitButton.grid(row=2, column=1)

    list(frame9, frame5, mycursor, username, buttFunction)


def delete(window, frame5, conn, mycursor, username):
    # Asks for platform and passwords, then finalise with OTP
    frame5.pack_forget()
    frame10 = tk.Frame(window)
    frame10.pack()

    def buttFunction(platform):
        # OTP window
        frame10.pack_forget()
        otpFrame = tk.Frame(window)
        otpFrame.pack()

        mycursor.execute("SELECT secretKey FROM Users WHERE username = %s", (username, ))
        row = mycursor.fetchone()
        if row:
            secretKey = row[0]
        else:
            tk.Label(frame10, text="*User not found!*", fg='#ff0000').pack()
            frame10.destroy()
            return

        # OTP Prompt
        otpT = tk.Label(otpFrame, text="Enter the OTP on Google Authenticator to verify you're the owner")
        otpT.grid(row=0, columnspan=2)
        otpTb = tk.Entry(otpFrame, show='*')
        otpTb.grid(row=1, columnspan=2)

        def verifyOTP():
            otp = otpTb.get()
            totp = pyotp.TOTP(secretKey)
            if totp.verify(otp):
                mycursor.execute("""DELETE FROM Images
                                    WHERE userId = (SELECT userId FROM Users WHERE Username = %s)
                                    AND platform = %s""",
                                    (username, platform))
                mycursor.execute("""DELETE FROM `keys`
                                    WHERE userId = (SELECT userId FROM Users WHERE Username = %s)
                                    AND platform = %s""",
                                    (username, platform))
                conn.commit() 
                successMB = messagebox.showinfo(title="Delete Image Successful", message=f"Image {platform} deleted!")
                returnMain(otpFrame, frame5)
            else:
                failMB = messagebox.showwarning(title="Delete Image Failed", message="*Invalid OTP. Please try again.*", fg='#ff0000')
                otpTb.delete(0, tk.END)

        # Return and submit button
        returnButt = Button(otpFrame, text='Return', command=lambda: returnMain(otpFrame, frame10))
        returnButt.grid(row=2, column=0)

        submitButt = Button(otpFrame, text='Submit', command=verifyOTP)
        submitButt.grid(row=2, column=1)

    list(frame10, frame5, mycursor, username, buttFunction)

############### End of Main Functions ###############
