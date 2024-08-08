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
        生成一个验证码
        Args:
            fonts: list: 字体列表，用于生成验证码，可随意
            file_path: str: 保存的文件路径
            format: str: 保存的文件格式
        """
        image = ImageCaptcha(fonts=fonts)
        character_library = {
            "Uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "Lowercase": "abcdefghijklmnopqrstuvwxyz",
            "Numbers": "0123456789"
        }
        # 生成一个6位验证码
        captcha_text = ""
        for i in range(6):
            library = character_library[choice(list(character_library.keys()))]
            captcha_text += choice(library)
        # 生成验证码图片
        data = image.generate(captcha_text, format=format)  # type: BytesIO
        with open(file_path, "wb") as f:
            f.write(data.getvalue())

    @staticmethod
    def audio_captcha(voices_dir: str, file_path="temp/captcha.wav"):
        warn("This feature has a bug and cannot be used, please wait for the fix.", DeprecationWarning)
        """
        生成一个音频验证码
        Args:
            voices_dir: str: 语音目录，用于生成验证码
            file_path: 保存的文件路径
        """
        audio = AudioCaptcha(voicedir=voices_dir)
        character_library = {
            "Uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "Lowercase": "abcdefghijklmnopqrstuvwxyz",
            "Numbers": "0123456789"
        }
        # 生成一个6位验证码
        captcha_text = ""
        for i in range(6):
            library = character_library[choice(list(character_library.keys()))]
            captcha_text += choice(library)
        # 生成验证码音频
        audio.write(captcha_text, output=file_path)


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("验证码生成器")
        self.geometry("300x300")
        self.resizable(False, False)
        self.style_set = ttk.Style("cosmo")
        self.main_title = ttk.Label(self, text="验证码生成器", font=("微软雅黑", 20))
        self.main_title.grid(columnspan=2, row=0, pady=10)
        self.options_frame = ttk.LabelFrame(self, text="选项")
        self.options_frame.grid(columnspan=2, row=1, pady=10)
        self.option = ttk.BooleanVar(self, value=True)
        self.picture_captcha_option = ttk.Radiobutton(self.options_frame, text="图片验证码", variable=self.option, value=True)
        self.picture_captcha_option.grid(column=0, row=0, padx=10, pady=5)
        self.audio_captcha_option = ttk.Radiobutton(self.options_frame, text="音频验证码", variable=self.option, value=False)
        self.audio_captcha_option.grid(column=1, row=0, padx=10, pady=5)
        self.generate_button = ttk.Button(self, text="生成", command=self.generate_captcha, bootstyle="success-outline")
        self.generate_button.grid(columnspan=2, row=2, pady=10)
        self.mainloop()

    def generate_captcha(self):
        if (self.option.get()):
            font_path = fdg.askopenfilenames(title="选择字体文件", filetypes=[("字体文件", ("*.ttf", "*.otf"))])
            if font_path:
                file_path = fdg.asksaveasfilename(title="保存验证码图片", filetypes=[("图片文件", "*.png")])
                if file_path:
                    format = file_path.split(".")[-1]
                    Make_Captcha.image_captcha(font_path, file_path, format=format)
                    msgbox.showinfo("提示", "验证码图片已生成！")
        else:
            msgbox.showwarning("警告", "此功能有bug，不能使用，请等待修复。")
#            voices_dir = fdg.askdirectory(title="选择源音频目录")
#            if voices_dir:
#                file_path = fdg.asksaveasfilename(title="保存音频验证码", filetypes=[("音频文件", "*.wav")])
#                if file_path:
#                    Make_Captcha.audio_captcha(voices_dir, file_path)
#                    msgbox.showinfo("提示", "音频验证码已生成！")


if __name__ == '__main__':
    App()
