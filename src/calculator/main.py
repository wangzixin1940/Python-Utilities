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
    ui = json.loads(ui_src_file)["externals"]["calculator"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


import math
import sys

import ttkbootstrap as ttk
from tkinter import messagebox as msgbox
from tkinter import Frame as tk_Frame


class Calculator(ttk.Window):
    def __init__(self):
        super().__init__()
        self.Buttons = [
            ["%", "CE", "C", "⏏"],
            ["1/x", "x^y", "2√x", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="]
        ]
        self.signs = ["%", "1/x", "x^y", "2√x", "/", "*", "-", "+", "±"]
        self.functions = ["CE", "C", "±", "=", "⏏"]
        self.data = []
        self.title(ui["title"])
        self.geometry("450x500")
        self.resizable(False, False)
        self.previous_type = None
        self.create_widgets()

    def create_widgets(self):
        self.result = tk_Frame(self, width=450, height=100)
        self.result.configure(bg="#F3F3F3")
        self.result.grid(column=0, row=0, columnspan=4, padx=5, pady=5)
        self.result_value = ttk.StringVar(value="".join(self.data))
        self.result_show = ttk.Label(
            self.result, textvariable=self.result_value, font=(
                "Airal", 20), anchor="e")
        self.result_show.grid(column=0, row=0, columnspan=4, padx=5, pady=5)
        self.button_frame = ttk.Frame(self, width=400, height=500)
        self.button_frame.grid(column=0, row=1, columnspan=4, padx=5, pady=5)
        # 创建按钮
        for i, row in enumerate(self.Buttons):
            for j, button_text in enumerate(row):
                button = ttk.Button(
                    self.button_frame,
                    text=button_text,
                    width=7,
                    command=lambda text=button_text: self.button_click(text),
                    bootstyle="primary-outline")
                button.grid(row=i, column=j, padx=5, pady=5)

    def button_click(self, text):
        if (text in self.functions):  # 功能
            match text:
                case "CE":
                    self.data.remove(self.data[-1])
                    self.result_value.set("".join(self.data))
                case "C":
                    self.data = []
                    self.result_value.set("".join(self.data))
                case "⏏":
                    if (msgbox.askyesno(ui["quit"]["title"], ui["quit"]["warn"])):
                        self.destroy()
                case "±":
                    if self.data[-1] in self.signs:
                        msgbox.showerror(
                            ui_src["error"], ui["positivityError"])
                    else:
                        self.data[-1] = str(-float(self.data[-1]))
                        self.result_value.set("".join(self.data))
                case "=":
                    try:
                        self.data = [str(eval("".join(self.data)))]
                        self.result_value.set("".join(self.data))
                    except ZeroDivisionError:
                        msgbox.showerror(ui_src["error"], ui["divideByZeroError"])
                        self.data = []
                    except ValueError:
                        msgbox.showerror(ui_src["error"], ui["overflowError"].format(max=str(sys.get_int_max_str_digits()) + "**10 - 1"))
                        self.data = []
                    except Exception as err:
                        msgbox.showerror(ui_src["error"], ui["expressionError"].format(repr(err)))
            self.previous_type = "function"
        elif (text in self.signs):  # 符号
            match text:
                case "1/x":
                    self.data[-1] = "1/" + str(self.data[-1])
                    self.result_value.set("".join(self.data))
                case "%":
                    self.data[-1] = str(float(self.data[-1]) / 100)
                    self.result_value.set("".join(self.data))
                case "x^y":
                    self.data.append("**")
                case "2√x":
                    self.data[-1] = str(float(math.sqrt(float(self.data[-1]))))
                case _:
                    self.data.append(text)
            self.previous_type = "sign"
        else:  # 数字
            if (self.previous_type == "number"):
                self.data[-1] = self.data[-1] + text
            else:
                self.data.append(text)
            self.result_value.set("".join(self.data))
            self.previous_type = "number"


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
