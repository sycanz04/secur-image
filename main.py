#! /usr/bin/env python3
from tkinter import *
import tkinter as tk
from utils.mainMenu import login, create, delete

window = tk.Tk()
window.title("Secur Image")
window.geometry('800x500')
frame1 = Frame(window)

def main():
    menuT = tk.Label(frame1, text="Select an option")
    menuT.pack()

    button1 = tk.Button(frame1, 
                        text="Login", command=lambda: login(window, frame1),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button1.pack()
    button2 = tk.Button(frame1, 
                        text="Signup", command=lambda: create(window, frame1),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button2.pack()
    button3 = tk.Button(frame1, 
                        text="Delete", command=lambda: delete(window, frame1),
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button3.pack()
    button4 = tk.Button(frame1, 
                        text="Quit", command=window.destroy,
                        activebackground="blue", activeforeground="white",
                        anchor="center", bd=3, bg="lightgray", cursor="hand2",
                        disabledforeground="gray", fg="black", font=("Arial", 12),
                        height=2, highlightbackground="black", highlightcolor="green",
                        highlightthickness=2, justify="center", overrelief="raised",
                        padx=10, pady=5, width=15, wraplength=100)
    button4.pack()

frame1.pack()
main()

window.mainloop()
