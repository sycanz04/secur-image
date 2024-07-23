# Secur-Image 🔒
Secur-Image was originally my project for [Hackerspace's](https://hackerspacemmu.rocks/) hackathon that I continued to work on after. The shortest way you could possible explain this program is it's a password manager.

## How does it work? 🧐
This program generate/insert(user input) a password, encrypts the password with RSA and stores half the private key in database and the other half on a flash drive. Then it signs the encrypted password with SHA-256 before embedding it into an image of user's choice with steganography technique (steghide). All while storing everything into a database.

## General program flow 🌊
User logs into their account (create if don't have one), prompted for MFA (TOTP), choose to insert/generate/decrypt passwords or list/delete image.

## Tech Stack ⚛️
Python (a couple pip libraries), Tkinter, MySQL
