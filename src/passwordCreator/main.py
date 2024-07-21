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
    length: 密码长度
    includeSymbols: 是否包含符号
    includeNumbers: 是否包含数字
    includeUppercase: 是否包含大写字母
    return: 返回密码字符串
    """
    # 密码字符集
    chars = {
        "lowers": "abcdefghijklmnopqrstuvwxyz",
        "uppers": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "numbers": "0123456789",
        "symbols": r"!\"#$%&'()*+,-./:;<=>?@[]^_{|}~"}
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
        password.insert(
            "1.0",
            passwordCreator(
                length.get(),
                includeSymbols.get(),
                includeNumbers.get(),
                includeUppercase.get()))
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
    symbols = ttk.Checkbutton(root, text="插入符号", variable=includeSymbols)
    numbers = ttk.Checkbutton(root, text="插入数字", variable=includeNumbers)
    uppercase = ttk.Checkbutton(root, text="插入大写字母", variable=includeUppercase)
    lowercase = ttk.Checkbutton(
        root,
        text="插入小写字母",
        variable=includeLowercase,
        state="disabled")
    symbols.pack(pady=5)
    numbers.pack(pady=5)
    uppercase.pack(pady=5)
    lowercase.pack(pady=5)
    generate = ttk.Button(
        root,
        text="生成",
        command=lambda: changeValue(),
        bootstyle="success-outline")
    generate.pack(pady=10)
    password = ttk.Text(root, width=30, height=5)
    password.config(state="disabled")
    password.pack(pady=10)
    copybtn = ttk.Button(
        root,
        text="复制",
        command=lambda: copyToClipboard(),
        bootstyle="outline-primary")
    copybtn.pack(pady=5)
    root.mainloop()


if __name__ == "__main__":
    main()
