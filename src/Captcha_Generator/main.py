from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha
from io import BytesIO
from random import choice

from ui.cg import Ui_MainWindow
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMessageBox, QStyleFactory, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator

import sys

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
    ui = json.loads(ui_src_file)["externals"]["captcha"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Define the variables
        self.choice = 0
        # Connect the button to the function
        self.pictureCaptchaChoice.clicked.connect(lambda: self.set_choice(0))
        self.audioCaptchaChoice.clicked.connect(lambda: self.set_choice(1))
        self.generateButton.clicked.connect(self.generate_captcha)

    def set_choice(self, choice):
        self.choice = choice

    def generate_captcha(self):
        if (self.choice == 0):
            font_path = QFileDialog.getOpenFileNames(self, ui["inputs"]["chooseFonts"], "", "Fonts(*.ttf; *.otf)")[0]
            if font_path:
                file_path = QFileDialog.getSaveFileName(self, ui["inputs"]["saveAs"], "", "Images(*.png)")[0]
                if file_path:
                    format = file_path.split(".")[-1]
                    Make_Captcha.image_captcha(font_path, file_path, format=format)
                    QMessageBox.information(self, ui_src["info"], ui["complete"])
        else:
            voices_dir = QFileDialog.getExistingDirectory(self, "选择源音频目录", "")[0]
            if voices_dir:
                file_path = QFileDialog.getSaveFileName(self, "保存音频验证码", "", "Audio(*.wav)")[0]
                if file_path:
                    Make_Captcha.audio_captcha(voices_dir, file_path)
                    QMessageBox.information(self, "提示", "音频验证码已生成！")


class Make_Captcha:
    @staticmethod
    def image_captcha(fonts: list, file_path="temp/captcha.png", format="png"):
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
        audio = AudioCaptcha(voicedir=voices_dir)
        character_library = {
            "Uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "Lowercase": "abcdefghijklmnopqrstuvwxyz",
            "Numbers": "0123456789"
        }
        # Generate a 6-digit verification code
        captcha_text = ""
        for i in range(6):
            library = character_library[choice(list(character_library.keys()))]
            captcha_text += choice(library)
        # Generate captcha audio
        audio.write(captcha_text, output=file_path)


if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    translator = QTranslator()
    if (translator.load(settings["qt_language"], directory="../../data/ui/i18n")):
        app.installTranslator(translator)
    window = App()
    window.setWindowIcon(QIcon("./image/favicon.ico"))
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec())
