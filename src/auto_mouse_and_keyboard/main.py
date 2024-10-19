import os
import json
os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["amk"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


import ttkbootstrap as ttk
import tkinter.filedialog as fdg
import tkinter.messagebox as msgbox
import traceback
import pynput
from pynput import mouse
from pynput import keyboard
from time import sleep as delay
from random import randint as rand


class Controllers:
    def __init(self):
        self.mouse = mouse.Controller()
        self.keybrd = keyboard.Controller()


class Functions:
    def __init__(self):
        self.mouse = pynput.mouse
        self.keybrd = pynput.keyboard

    @staticmethod
    def delay(*args, **kwargs):
        return delay(*args, **kwargs)

    @staticmethod
    def rand(*args, **kwargs):
        return rand(*args, **kwargs)


Controllers = Controllers()
Functions = Functions()

# 可用的方法：mouse, keyboard, delay, rand

# mouse, keybrd 语法见 https://pynput.readthedocs.io/en/latest/index.html

# delay 语法：
# delay(sec: int)
# 等待 sec 秒

# rand 语法：
# rand(min: int, max: int)
# 在 min 到 max 之间随机取一个数

mouse = mouse.Controller()
keyboard = keyboard.Controller()


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Auto Mouse and Keyboard")
        self.geometry("400x300")
        self.resizable(False, False)
        self.main_title = ttk.Label(
            self, text="Auto Mouse and Keyboard", font=(
                "Arial", 20))
        self.file = ttk.StringVar(value=ui["open"])
        self.input_file = ttk.Button(
            self,
            textvariable=self.file,
            command=self.open_file,
            width=15,
            bootstyle="primary-outline")
        self.doWork_btn = ttk.Button(
            self,
            text=ui["launch"],
            command=self.doWork,
            width=15,
            bootstyle="success-outline")
        self.main_title.pack(pady=20)
        self.input_file.pack(pady=10)
        self.doWork_btn.pack(pady=10)
        self.mainloop()

    def open_file(self):
        self.file.set(
            fdg.askopenfilename(
                title=ui["open"], filetypes=[
                    file_types["amk"], file_types["py"]]))

    def doWork(self):
        if self.file.get() != ui["open"]:
            with open(self.file.get(), "r", encoding="utf-8") as f:
                data = f.read()
                if (data.startswith("#-- ENABLE --#")):
                    try:
                        exec(data)
                    except Exception as e:
                        msgbox.showerror(
                            ui_src["error"], f"{ui["err"]}\n{
                                repr(e)}：\n{
                                traceback.print_exc()}")
                else:
                    msgbox.showerror(
                        ui_src["error"], ui["notEnable"])
        else:
            msgbox.showerror(ui_src["error"], ui["fileNotFound"])


if __name__ == "__main__":
    App()
