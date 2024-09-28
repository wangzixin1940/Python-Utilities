from tkinter import filedialog as fd
from ocr import read_text_from_image as ocr
import ttkbootstrap as ttk
import os
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# 更换编码

os.chdir(os.path.dirname(__file__))
# 更换工作目录

import json

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["ocr"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title(ui["title"])
        self.geometry("400x600")
        self.resizable(True, True)
        self.iconbitmap("assets/favicon.ico")
        self.resizable(False, False)
        self.styleset = ttk.Style()
        self.styleset.configure(
            "TButton",
            font=("Helvetica", 18, "normal"),
            width=20, height=3)
        # 创建控件
        self.maintitle = ttk.Label(
            self, text=ui["title"], font=(
                "Helvetica", 20, "normal"))
        self.maintitle.pack(pady=10)
        self.image_choose_button = ttk.Button(
            self,
            text=ui["chooseImage"],
            command=self.chooseImage,
            width=10,
            bootstyle="primary-outline")
        self.image_choose_button.pack(pady=10)
        # 创建识别按钮
        self.recognize_button = ttk.Button(
            self,
            text=ui["recognize"],
            command=self.recognize,
            width=10,
            bootstyle="success-outline")
        self.recognize_button.pack(pady=10, side="top", anchor="center")
        # 创建结果标签
        self.result_label = ttk.Label(
            self, text=ui["result"], font=(
                "Helvetica", 16, "normal"))
        self.result_label.pack(pady=10)
        # 创建结果文本框
        self.result_textbox = ttk.ScrolledText(self)
        self.result_textbox.configure(state="disabled")
        self.result_textbox.pack(pady=10)
        # 主循环
        self.mainloop()

    def chooseImage(self):
        self.image = fd.askopenfilename(
            filetypes=[file_types["images"]["jpg"], file_types["images"]["png"], file_types["images"]["bmp"]])
        self.image_choose_button.configure(
            text=ui["choosed"], bootstyle="success-outline")

    def recognize(self):
        result = ocr(self.image)
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", ttk.END)
        self.result_textbox.insert(ttk.END, result)
        self.result_textbox.configure(state="disabled")


if __name__ == "__main__":
    app = App()
