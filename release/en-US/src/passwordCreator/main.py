import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
# Change Encoding to UTF-8

import os
os.chdir(os.path.dirname(__file__))
# Change Directory to Current File


import logging
import datetime
import random
import ttkbootstrap as ttk
from tkinter import messagebox as msgbox
import pyperclip as cb
import json

with open("../../data/settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

if not(settings["no-log-file"]):
    logging.basicConfig(
                    filename=f"../../logs/{datetime.date.today()}.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
    )
else:
    logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - NO-LOG-FILE - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
    )
logger = logging.getLogger("PWDCTR")


def passwordCreator(length:int, includeSymbols:bool=False, includeNumbers:bool=True, includeUppercase:bool=True):
        """
        length: Password Length
        includeSymbols: OK to include symbols
        includeNumbers: OK to include numbers
        includeUppercase: OK to include uppercase
        return: Password String
        """
        # Password Charset
        chars = {"lowers":"abcdefghijklmnopqrstuvwxyz", "uppers":"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "numbers":"0123456789", "symbols":r"!\"#$%&'()*+,-./:;<=>?@[]^_{|}~"}
        if not includeSymbols: del chars["symbols"]
        if not includeNumbers: del chars["numbers"]
        if not includeUppercase: del chars["uppers"]
        password = ""
        try :
            for i in range(int(length)):
                # Randomly choose a charset
                charset = random.choice(list(chars.keys()))
                # Randomly choose a character from the charset
                char = random.choice(chars[charset])
                # Add the character to the password
                password += char
            return password
        except KeyError as err:
            logger.error(f"KEY ERROR: {err}")
            return 1
        except Exception as err:
            logger.error(f"ERROR: {err}")
            raise err


def main():
    def copyToClipboard():
        if password.get("1.0", "end") == "":
            msgbox.showerror("Error", "No password to copy!")
            return 1
        cb.copy(str(password.get("1.0", "end")))
        msgbox.showinfo("Copied", "Password copied to clipboard!")
        return 0
    def changeValue():
        password.config(state="normal")
        password.delete("1.0", "end")
        password.insert("1.0", passwordCreator(length.get(), includeSymbols.get(), includeNumbers.get(), includeUppercase.get()))
        password.config(state="disabled")

    root = ttk.Window("Password Creator", "cosmo")
    root.geometry("400x550")
    root.resizable(False, False)
    root.iconbitmap("./assets/icon.ico")
    root.title("Password Creator")
    title = ttk.Label(root, text="Password Creator", font=("Arial", 20))
    title.pack(pady=10)
    length = ttk.Spinbox(root, from_=4, to=32, width=10)
    length.set(10)
    length.pack(pady=5)
    includeSymbols = ttk.BooleanVar(value=True)
    includeNumbers = ttk.BooleanVar(value=True)
    includeUppercase = ttk.BooleanVar(value=True)
    includeLowercase = ttk.BooleanVar(value=True)
    symbols = ttk.Checkbutton(root, text="Insert Symbols", variable=includeSymbols)
    numbers = ttk.Checkbutton(root, text="Insert Numbers", variable=includeNumbers)
    uppercase = ttk.Checkbutton(root, text="Insert Uppercase", variable=includeUppercase)
    lowercase = ttk.Checkbutton(root, text="Insert Lowercase", variable=includeLowercase, state="disabled")
    symbols.pack(pady=5)
    numbers.pack(pady=5)
    uppercase.pack(pady=5)
    lowercase.pack(pady=5)
    generate = ttk.Button(root, text="Generate", command=lambda:changeValue(), bootstyle="success-outline")
    generate.pack(pady=10)
    password = ttk.Text(root, width=30, height=5)
    password.config(state="disabled")
    password.pack(pady=10)
    copybtn = ttk.Button(root, text="Copy", command=lambda:copyToClipboard(), bootstyle="outline-primary")
    copybtn.pack(pady=5)
    root.mainloop()


if __name__ == "__main__":
    main()