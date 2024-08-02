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
    def __init(self, *args, **kwargs):
        self.mouse = mouse.Controller()
        self.keybrd = keyboard.Controller()


class Functions:
    def __init__(self, *args, **kwargs):
        self.mouse = pynput.mouse
        self.keybrd = pynput.keyboard

    def delay(self, *args, **kwargs):
        return delay(*args, **kwargs)

    def rand(self, *args, **kwargs):
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
        self.file = ttk.StringVar(value="打开文件")
        self.input_file = ttk.Button(
            self,
            textvariable=self.file,
            command=self.open_file,
            width=15,
            bootstyle="primary-outline")
        self.do_work_btn = ttk.Button(
            self,
            text="启动",
            command=self.do_work,
            width=15,
            bootstyle="success-outline")
        self.main_title.pack(pady=20)
        self.input_file.pack(pady=10)
        self.do_work_btn.pack(pady=10)
        self.mainloop()

    def open_file(self):
        self.file.set(
            fdg.askopenfilename(
                title="打开文件", filetypes=[
                    ("AMK Script", "*.amk"), ("Python Script", "*.py")]))

    def do_work(self):
        if self.file.get() != "打开文件":
            with open(self.file.get(), "r", encoding="utf-8") as f:
                data = f.read()
                if (data.startswith("#-- ENABLE --#")):
                    try:
                        exec(data)
                    except Exception as e:
                        msgbox.showerror(
                            "错误", f"执行脚本时发生错误：\n{
                                repr(e)}：\n{
                                traceback.print_exc()}")
                else:
                    msgbox.showerror(
                        "错误", "脚本被禁用！\n请在脚本开头添加：\n#-- ENABLE --#\n或将#-- DISABLE --#替换成#-- ENABLE --#")
        else:
            msgbox.showerror("错误", "请先选择文件！")


if __name__ == "__main__":
    App()
