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
# 更换编码

os.chdir(os.path.dirname(__file__))
# 更换工作目录


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


def passwordCreator(
        length: int,
        includeSymbols: bool = False,
        includeNumbers: bool = True,
        includeUppercase: bool = True):
    """
    生成密码
    参数：
        length: 密码长度
        includeSymbols: 是否包含符号
        includeNumbers: 是否包含数字
        includeUppercase: 是否包含大写字母
    返回值：返回密码字符串
    """
    # 密码字符集
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
            # 随机选择一个字符集
            charset = random.choice(list(chars.keys()))
            # 随机选择一个字符
            char = random.choice(chars[charset])
            # 添加到密码字符串
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
        msgbox.showinfo("Copied", "Password copied to clipboard!")
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
        strength = {
            1: "弱",
            2: "中等",
            3: "强",
            4: "很强"
        }
        self.strengthTips["text"] = "密码强度：" + strength[self.strengthCheck(str(self.password.get("1.0", "end")))]

    def __init__(self):
        super().__init__()
        self.title("Password Creator")
        self.style_set = ttk.Style(theme="cosmo")
        self.geometry("400x550")
        self.resizable(False, False)
        self.iconbitmap("./assets/icon.ico")
        self.title("Password Creator")
        self.main_title = ttk.Label(self, text="Password Creator", font=("Arial", 20))
        self.main_title.pack(pady=10)
        self.length = ttk.Spinbox(self, from_=4, to=32, width=10)
        self.length.set(10)
        self.length.pack(pady=5)
        self.includeSymbols = ttk.BooleanVar(value=True)
        self.includeNumbers = ttk.BooleanVar(value=True)
        self.includeUppercase = ttk.BooleanVar(value=True)
        self.includeLowercase = ttk.BooleanVar(value=True)
        self.symbols = ttk.Checkbutton(self, text="插入符号", variable=self.includeSymbols)
        self.numbers = ttk.Checkbutton(self, text="插入数字", variable=self.includeNumbers)
        self.uppercase = ttk.Checkbutton(self, text="插入大写字母", variable=self.includeUppercase)
        self.lowercase = ttk.Checkbutton(
            self,
            text="插入小写字母",
            variable=self.includeLowercase,
            state="disabled")
        self.symbols.pack(pady=5)
        self.numbers.pack(pady=5)
        self.uppercase.pack(pady=5)
        self.lowercase.pack(pady=5)
        self.generate = ttk.Button(
            self,
            text="生成",
            command=lambda: self.changeValue(),
            bootstyle="success-outline")
        self.generate.pack(pady=10)
        self.password = ttk.Text(self, width=30, height=5)
        self.password.config(state="disabled")
        self.password.pack(pady=10)
        self.strengthTips = ttk.Label(self, text="密码强度：未知")
        self.strengthTips.pack(pady=5)
        self.copybtn = ttk.Button(
            self,
            text="复制",
            command=lambda: self.copyToClipboard(),
            bootstyle="outline-primary")
        self.copybtn.pack(pady=5)
        self.mainloop()


if __name__ == "__main__":
    App()
