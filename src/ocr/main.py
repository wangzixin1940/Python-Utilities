import os
import io
import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
import easyocr

from ui.ocr import Ui_MainWindow as MainWindow

import json

os.chdir(os.path.dirname(__file__))
# 更换工作目录

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# 更换编码

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file


def recognition(reader: easyocr.Reader, image_path):
    """
    Use the EasyOCR library to extract text from images.
    Args:
        reader: EasyOCR reader
        image_path: Image file path
    Returns:
        Results
    """
    return reader.readtext((image_path), detail=0)


class App(QtWidgets.QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Define the variables
        self.filePath = ""
        self.result = []
        self.reader = None
        # Connect the buttons to the functions
        self.choosePictureButton.clicked.connect(self.choose_picture)
        self.identifyButton.clicked.connect(self.identify)

    def choose_picture(self):
        self.filePath = QFileDialog.getOpenFileName(self, "Choose a photo", "", "Image(*.jpg *.png)")[0]
        if self.filePath:
            self.choosePictureButton.setText(self.filePath)

    def identify(self):
        if not self.reader:
            self.reader = easyocr.Reader(['en', 'ch_sim'], gpu=True)
            # Use English and Chinese Simplified Chinese models
        self.result = recognition(self.reader, self.filePath)
        self.resultDisplay.setPlainText("\n".join(self.result))


if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    translator = QTranslator()
    if (translator.load(settings["qt_language"], directory="../../data/ui/i18n")):
        app.installTranslator(translator)
    window = App()
    window.setWindowIcon(QIcon("./images/favicon.ico"))
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec())
