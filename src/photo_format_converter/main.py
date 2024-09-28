from tkinter import messagebox as msgbox
from tkinter import filedialog as fdg
import ttkbootstrap as ttk
from PIL import Image
import os

os.chdir(os.path.dirname(__file__))
# Change the working directory to the current file's directory

import json

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["photo_format_convertor"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title(ui["title"])
        self.geometry("450x300")
        self.resizable(False, False)
        self.style_set = ttk.Style()
        self.style_set.theme_use("cosmo")
        self.style_set.configure("TButton", font=("Arial", 12), width=20)
        self.iconbitmap("assets/favicon.ico")
        # Create widgets
        self.main_title = ttk.Label(
            self, text=ui["title"], font=(
                "Arial", 20))
        self.main_title.pack(pady=10)
        self.image_path = ttk.StringVar(value=ui["choosePhoto"])
        self.input_button = ttk.Button(
            self, textvariable=self.image_path, command=self.open_file)
        self.input_button.pack(pady=10)
        self.convert_button = ttk.Button(self, text=ui["convert"], command=self.convert)
        self.convert_button.pack(pady=10)
        # Main loop
        self.mainloop()

    def open_file(self):
        file_path = fdg.askopenfilename(
            filetypes=[file_types["images"]["jpg"], file_types["images"]["png"], file_types["images"]["bmp"], file_types["images"]["gif"]])
        if file_path:
            self.image_path.set(file_path)

    def convert(self):
        if self.image_path.get() == ui["choosePhoto"]:
            msgbox.showwarning(ui_src["warn"], ui["noPictureSelectedError"])
            return
        image = Image.open(self.image_path.get())
        output = fdg.asksaveasfilename(
            defaultextension=".jpg", filetypes=[file_types["images"]["jpg"], file_types["images"]["png"], file_types["images"]["bmp"], file_types["images"]["gif"]])
        if output:
            image.save(output)
            msgbox.showinfo(ui_src["info"], ui["complete"])
            return


if __name__ == "__main__":
    App()
