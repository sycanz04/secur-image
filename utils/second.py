from utils.secondMenu import insert, generate, decrypt, list, delete
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
                        text="Generate",
                        command=lambda: generate(window, frame5, conn, mycursor, username),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button2.pack()
    button3 = tk.Button(frame5,
                        text="Decrypt",
                        command=lambda: decrypt(window, frame5, conn, mycursor, username),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button3.pack()
    button4 = tk.Button(frame5,
                        text="List Image",
                        command=lambda: list(window, frame5, conn, mycursor, username),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button4.pack()
    button5 = tk.Button(frame5,
                        text="Delete Image",
                        command=lambda: delete(window, frame5, conn, mycursor, username),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button5.pack()
    button6 = tk.Button(frame5,
                        text="Quit", command=window.destroy,
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button6.pack()
