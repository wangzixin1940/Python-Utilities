from send import Send
import ttkbootstrap as ttk
from tkinter import filedialog as fdg
from tkinter import messagebox as msgbox

import os
import json

os.chdir(os.path.dirname(__file__))
# 更换工作目录

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["send_mail_from_json"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title(ui["title"])
        self.geometry("400x300")
        self.resizable(False, False)
        self.style_set = ttk.Style("cosmo")
        self.style_set.configure("TButton", font=("Arial", 14), width=20)
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        self.main_title = ttk.Label(
            self, text=ui["title"], font=(
                "Arial", 20))
        self.main_title.pack(pady=10)
        self.json_file = ttk.StringVar(value=ui["choose_file"])
        self.choose_file_button = ttk.Button(
            self,
            textvariable=self.json_file,
            command=self.choose_file,
            bootstyle="primary-outline")
        self.choose_file_button.pack(pady=10)
        self.send_button = ttk.Button(
            self,
            text=ui["send"],
            command=self.send_mail,
            bootstyle="success-outline")
        self.send_button.pack(pady=10)

    def choose_file(self):
        self.json_file.set(
            fdg.askopenfilename(
                filetypes=[file_types["json"]]))

    def send_mail(self):
        if (self.json_file.get() != ui["choose_file"]):
            Send(self.json_file.get())
            msgbox.showinfo(ui["success"], ui["success_info"])
        else:
            msgbox.showerror(ui_src["error"], ui["error_info"])


if __name__ == "__main__":
    App()
