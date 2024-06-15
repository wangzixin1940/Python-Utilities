import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
# Change the encoding of the standard output to UTF-8

import os
os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script


import ttkbootstrap as ttk
from ocr import read_text_from_image as ocr
from tkinter import filedialog as fd

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Character Recognizer")
        self.geometry("400x600")
        self.resizable(True, True)
        self.iconbitmap("assets/favicon.ico")
        self.resizable(False, False)
        self.styleset = ttk.Style()
        self.styleset.configure("TButton", font=("Helvetica", 18, "normal"), width=20, height=3)
        # Create widgets
        self.maintitle = ttk.Label(self, text="Character Recognizer", font=("Helvetica", 20, "normal"))
        self.maintitle.pack(pady=10)
        self.image_choose_button = ttk.Button(self, text="Choose Image", command=self.choose_image, width=10, bootstyle="primary-outline")
        self.image_choose_button.pack(pady=10)
        # Create a button to start the OCR process
        self.recognize_button = ttk.Button(self, text="Recognize", command=self.recognize, width=10, bootstyle="success-outline")
        self.recognize_button.pack(pady=10, side="top", anchor="center")
        # Create a label for the result
        self.result_label = ttk.Label(self, text="Result:", font=("Helvetica", 16, "normal"))
        self.result_label.pack(pady=10)
        # Create a result text box
        self.result_textbox = ttk.ScrolledText(self)
        self.result_textbox.configure(state="disabled")
        self.result_textbox.pack(pady=10)
        # Main loop
        self.mainloop()
    
    def choose_image(self):
        self.image = fd.askopenfilename(filetypes=[("Image Files", ("*.jpg", "*.png", "*.bmp"))])
        self.image_choose_button.configure(text="Choosed", bootstyle="success-outline")

    def recognize(self):
        result = ocr(self.image)
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", ttk.END)
        self.result_textbox.insert(ttk.END, result)
        self.result_textbox.configure(state="disabled")

if __name__ == "__main__":
    app = App()

