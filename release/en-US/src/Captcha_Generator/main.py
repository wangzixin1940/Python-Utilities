from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha
from io import BytesIO
from random import choice
import ttkbootstrap as ttk
from tkinter import filedialog as fdg
from tkinter import messagebox as msgbox
from warnings import warn


class Make_Captcha:
    @staticmethod
    def image_captcha(fonts: list, file_path="temp/captcha.png", format="png"):
        """
        Generate a captcha
        Args:
            fonts: list: A list of fonts to generate a captcha
            file_path: str: The path to the saved file
            format: str: Saved file format
        """
        image = ImageCaptcha(fonts=fonts)
        character_library = {
            "Uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "Lowercase": "abcdefghijklmnopqrstuvwxyz",
            "Numbers": "0123456789"
        }
        # Generate a 6-digit captcha
        captcha_text = ""
        for i in range(6):
            library = character_library[choice(list(character_library.keys()))]
            captcha_text += choice(library)
        # Generate a captcha image
        data = image.generate(captcha_text, format=format)  # type: BytesIO
        with open(file_path, "wb") as f:
            f.write(data.getvalue())

    @staticmethod
    def audio_captcha(voices_dir: str, file_path="temp/captcha.wav"):
        warn("This feature has a bug and cannot be used, please wait for the fix.", DeprecationWarning)
        """
        Generate an audio verification code
        Args:
            voices_dir: str: Voice directory to generate captcha
            file_path: The path to the saved file
        """
        audio = AudioCaptcha(voicedir=voices_dir)
        character_library = {
            "Uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "Lowercase": "abcdefghijklmnopqrstuvwxyz",
            "Numbers": "0123456789"
        }
        # Generate a 6-digit captcha
        captcha_text = ""
        for i in range(6):
            library = character_library[choice(list(character_library.keys()))]
            captcha_text += choice(library)
        # Generate captcha audio
        audio.write(captcha_text, output=file_path)


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Captcha Generator")
        self.geometry("300x300")
        self.resizable(False, False)
        self.style_set = ttk.Style("cosmo")
        self.main_title = ttk.Label(self, text="Captcha Generator", font=("Airal", 20))
        self.main_title.grid(columnspan=2, row=0, pady=10)
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.grid(columnspan=2, row=1, pady=10)
        self.option = ttk.BooleanVar(self, value=True)
        self.picture_captcha_option = ttk.Radiobutton(self.options_frame, text="Image captcha", variable=self.option, value=True)
        self.picture_captcha_option.grid(column=0, row=0, padx=10, pady=5)
        self.audio_captcha_option = ttk.Radiobutton(self.options_frame, text="Audio captcha", variable=self.option, value=False)
        self.audio_captcha_option.grid(column=1, row=0, padx=10, pady=5)
        self.generate_button = ttk.Button(self, text="GENERATE", command=self.generate_captcha, bootstyle="success-outline")
        self.generate_button.grid(columnspan=2, row=2, pady=10)
        self.mainloop()

    def generate_captcha(self):
        if (self.option.get()):
            font_path = fdg.askopenfilenames(title="Select the font file", filetypes=[("Font files", ("*.ttf", "*.otf"))])
            if font_path:
                file_path = fdg.asksaveasfilename(title="Save the captcha image", filetypes=[("Image files", "*.png")])
                if file_path:
                    format = file_path.split(".")[-1]
                    Make_Captcha.image_captcha(font_path, file_path, format=format)
                    msgbox.showinfo("Information", "Captcha image has been generated!")
        else:
            msgbox.showwarning("Warning", "This feature has a bug and cannot be used, please wait for the fix.")
#            voices_dir = fdg.askdirectory(title="Select the source audio catalog")
#            if voices_dir:
#                file_path = fdg.asksaveasfilename(title="Save the audio captcha", filetypes=[("Audio files", "*.wav")])
#                if file_path:
#                    Make_Captcha.audio_captcha(voices_dir, file_path)
#                    msgbox.showinfo("Information", "Audio captcha has been generated!")


if __name__ == '__main__':
    App()
