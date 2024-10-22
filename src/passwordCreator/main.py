import json
import pyperclip as cb
from tkinter import messagebox as msgbox
import ttkbootstrap as ttk
import random
import datetime
import logging
import os
import io
import sys
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
# Change the encoding of the console output to utf-8

os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script


with open("../../data/settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

if not (settings["no-log-file"]):
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


import json

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["passwordCreator"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


def passwordCreator(
        length: int,
        includeSymbols: bool = False,
        includeNumbers: bool = True,
        includeUppercase: bool = True):
    """
    Generate passwords
    Args:
        length: Password length
        includeSymbols: Whether to include symbols
        includeNumbers: Whether to include numbers
        includeUppercase: Whether to include capital letters
    Returns:
        Password string
    """
    # Password character set
    chars = {
        "lowers": "abcdefghijklmnopqrstuvwxyz",
        "uppers": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "numbers": "0123456789",
        "symbols": r"!\"#$%&'()*+,-./:;<=>?@[]^_{|}~"
    }
    if not includeSymbols:
        del chars["symbols"]
    if not includeNumbers:
        del chars["numbers"]
    if not includeUppercase:
        del chars["uppers"]
    password = ""
    try:
        for i in range(int(length)):
            # A character set is selected at random
            charset = random.choice(list(chars.keys()))
            # Choose a character at random
            char = random.choice(chars[charset])
            # Add to the password string
            password += char
        return password
    except KeyError as err:
        logger.error(f"Key Error: {err}")
        return 1
    except Exception as err:
        logger.error(f"Error: {err}")
        raise err


class App(ttk.Window):

    @staticmethod
    def strengthCheck(password: str):
        if (len(password) < 8):
            return 1
        else:
            if (not re.search("[A-Z]", password)):
                return 2
            else:
                if (not re.search("[^a-zA-Z0-9]", password)):
                    return 3
                else:
                    return 4

    def copyToClipboard(self):
        if self.password.get("1.0", "end") == "":
            msgbox.showerror("Error", "No password to copy!")
            return 1
        cb.copy(str(self.password.get("1.0", "end")))
        msgbox.showinfo(ui["copied"], ui["completeInformation"])
        return 0

    def changeValue(self):
        self.password.config(state="normal")
        self.password.delete("1.0", "end")
        self.password.insert(
            "1.0",
            passwordCreator(
                self.length.get(),
                self.includeSymbols.get(),
                self.includeNumbers.get(),
                self.includeUppercase.get()))
        self.password.config(state="disabled")
        strength = ui["strength"]
        self.strengthTips["text"] = ui["passwordStrength"] + strength[self.strengthCheck(str(self.password.get("1.0", "end")))]

    def __init__(self):
        super().__init__()
        self.title(ui["title"])
        self.style_set = ttk.Style(theme="cosmo")
        self.geometry("400x550")
        self.resizable(False, False)
        self.iconbitmap("./assets/icon.ico")
        self.title(ui["title"])
        self.main_title = ttk.Label(self, text=ui["title"], font=("Arial", 20))
        self.main_title.pack(pady=10)
        self.length = ttk.Spinbox(self, from_=4, to=32, width=10)
        self.length.set(10)
        self.length.pack(pady=5)
        self.includeSymbols = ttk.BooleanVar(value=True)
        self.includeNumbers = ttk.BooleanVar(value=True)
        self.includeUppercase = ttk.BooleanVar(value=True)
        self.includeLowercase = ttk.BooleanVar(value=True)
        self.symbols = ttk.Checkbutton(self, text=ui["inclubes"]["symbols"], variable=self.includeSymbols)
        self.numbers = ttk.Checkbutton(self, text=ui["inclubes"]["numbers"], variable=self.includeNumbers)
        self.uppercase = ttk.Checkbutton(self, text=ui["inclubes"]["uppers"], variable=self.includeUppercase)
        self.lowercase = ttk.Checkbutton(
            self,
            text=ui["inclubes"]["lowers"],
            variable=self.includeLowercase,
            state="disabled")
        self.symbols.pack(pady=5)
        self.numbers.pack(pady=5)
        self.uppercase.pack(pady=5)
        self.lowercase.pack(pady=5)
        self.generate = ttk.Button(
            self,
            text=ui["create"],
            command=lambda: self.changeValue(),
            bootstyle="success-outline")
        self.generate.pack(pady=10)
        self.password = ttk.Text(self, width=30, height=5)
        self.password.config(state="disabled")
        self.password.pack(pady=10)
        self.strengthTips = ttk.Label(self, text=ui["passwordStrength"]+ui["unknown"])
        self.strengthTips.pack(pady=5)
        self.copybtn = ttk.Button(
            self,
            text=ui["copy"],
            command=lambda: self.copyToClipboard(),
            bootstyle="outline-primary")
        self.copybtn.pack(pady=5)
        self.mainloop()


if __name__ == "__main__":
    App()
