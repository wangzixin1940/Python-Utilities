import os
os.chdir(os.path.dirname(__file__))
# Change the working directory to the current file's directory

import PIL
import ttkbootstrap as ttk
from tkinter import filedialog as fdg
from tkinter import messagebox as msgbox

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Photo Format Converter")
        self.geometry("450x300")
        self.resizable(False, False)
        self.style_set = ttk.Style()
        self.style_set.theme_use("cosmo")
        self.style_set.configure("TButton", font=("Arial", 12), width=20)
        self.iconbitmap("assets/favicon.ico")
        # Create widgets
        self.main_title = ttk.Label(self, text="Photo Format Converter", font=("Arial", 20))
        self.main_title.pack(pady=10)
        self.image_path = ttk.StringVar(value="Choose a file")
        self.input_button = ttk.Button(self, textvariable=self.image_path, command=self.open_file)
        self.input_button.pack(pady=10)
        self.convert_button = ttk.Button(self, text="Convert", command=self.convert)
        self.convert_button.pack(pady=10)
        # Main loop
        self.mainloop()

    def open_file(self):
        file_path = fdg.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if file_path:
            self.image_path.set(file_path)
        
    def convert(self):
        if self.image_path.get() == "Choose a file":
            msgbox.showwarning("Warning", "Please choose a file first!")
            return
        image = PIL.Image.open(self.image_path.get())
        output = fdg.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("GIF", "*.gif")])
        if output:
            image.save(output)
            msgbox.showinfo("Info", "Conversion complete!")
            return


if __name__ == "__main__":
    App()
