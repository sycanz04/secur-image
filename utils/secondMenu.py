from tkinter import *
from tkinter import filedialog
import tkinter as tk
from utils.ls import listImage


################## Basic Functions ##################

# Prompts user for platform name
def prompt(frames):
    platformT = tk.Label(frames, text="Platform")
    platformT.grid(row=0, column=0)

    platformTb = Entry(frames)
    platformTb.grid(row=0, column=1)

    return platformTb

# Prompts user for passwd
def getPasswd(frames):
    passwdT = tk.Label(frames, text="Password")
    passwdT.grid(row=1, column=0)

    passwdTb = Entry(frames, show='*')
    passwdTb.grid(row=1, column=1)

    return passwdTb

# Return to previous frame
def returnMain(curFrame, mainFrame):
    curFrame.destroy()
    mainFrame.pack()

# Choose image file path
def chooseFile(fileLabel):
    filePath = filedialog.askopenfilename(title="Select an image")
    if filePath:
        fileLabel.config(text=f"Selected file: {filePath}")

    return filePath

############# End of Basic Functions ###############

################## Main Functions ##################

def insert(window, frame5, conn, mycursor, username):
    frame5.pack_forget()
    frame7 = Frame(window)
    frame7.pack()

    # Get platform name and passwd
    platform = prompt(frame7)
    passwd = getPasswd(frame7)

    # Labels to display selected paths
    fileLabel = tk.Label(frame7, text="No file selected")
    fileLabel.grid(row=2, column=0)

    # Choose an image
    fileButt = tk.Button(frame7, text="Choose File",
                         command=lambda: chooseFile(fileLabel))
    fileButt.grid(row=2, column=1)

    def handleInsert():
        userPlatform = platform.get()
        userPasswd = passwd.get()
        fileName = fileLabel.cget("text")

        # Remove any existing error message
        for widget in frame7.grid_slaves(row=4):
            widget.destroy()

        if not userPlatform or not userPasswd or "No file selected" in fileName:
            errorT = tk.Label(frame7, text="*All fields are required!*", fg='#ff0000')
            errorT.grid(row=4, column=0, columnspan=2)
            return

    cancelButton = tk.Button(frame7, text="Cancel",
                             command=lambda: returnMain(frame7, frame5))
    cancelButton.grid(row=3, column=0)

    submitButton = tk.Button(frame7, text="Done",
                             command=handleInsert)
    submitButton.grid(row=3, column=1)

    #enc(userPasswd, userPlatform, conn, mycursor, username):


def list(window, frame5, conn, mycursor, username):
    frame5.pack_forget()
    frame6 = Frame(window)
    frame6.pack()

    # Display username
    userT = tk.Label(frame6, text=username)
    userT.pack(padx=10, pady=10)

    success, result = listImage(conn, mycursor, username)
    if success:
        for imgId, platform in result:
            imgList = tk.Label(frame6, text=f"Image ID: {imgId}, Platform: {platform}")
            imgList.pack()
    else:
        errorLabel = tk.Label(frame6, text=result, fg='#ff0000')
        errorLabel.pack()

    returnButton = tk.Button(frame6,
                             text='Return',
                             command=lambda: returnMain(frame6, frame5))
    returnButton.pack()

############### End of Main Functions ###############
