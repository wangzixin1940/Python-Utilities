import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
# 更换编码

import os
os.chdir(os.path.dirname(__file__))
# 更换工作目录


import ttkbootstrap as ttk
from ocr import read_text_from_image as ocr
from tkinter import filedialog as fd

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("文字识别器")
        self.geometry("400x600")
        self.resizable(True, True)
        self.iconbitmap("assets/favicon.ico")
        self.resizable(False, False)
        self.styleset = ttk.Style()
        self.styleset.configure("TButton", font=("等线 Light", 18, "normal"), width=20, height=3)
        # 创建控件
        self.maintitle = ttk.Label(self, text="文字识别器", font=("等线 Light", 20, "normal"))
        self.maintitle.pack(pady=10)
        self.image_choose_button = ttk.Button(self, text="选择图片", command=self.choose_image, width=10, bootstyle="primary-outline")
        self.image_choose_button.pack(pady=10)
        # 创建识别按钮
        self.recognize_button = ttk.Button(self, text="识别", command=self.recognize, width=10, bootstyle="success-outline")
        self.recognize_button.pack(pady=10, side="top", anchor="center")
        # 创建结果标签
        self.result_label = ttk.Label(self, text="识别结果:", font=("等线 Light", 16, "normal"))
        self.result_label.pack(pady=10)
        # 创建结果文本框
        self.result_textbox = ttk.ScrolledText(self)
        self.result_textbox.configure(state="disabled")
        self.result_textbox.pack(pady=10)
        # 主循环
        self.mainloop()
    
    def choose_image(self):
        self.image = fd.askopenfilename(filetypes=[("图片文件", ("*.jpg", "*.png", "*.bmp"))])
        self.image_choose_button.configure(text="已选择", bootstyle="success-outline")

    def recognize(self):
        result = ocr(self.image)
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", ttk.END)
        self.result_textbox.insert(ttk.END, result)
        self.result_textbox.configure(state="disabled")

if __name__ == "__main__":
    app = App()

