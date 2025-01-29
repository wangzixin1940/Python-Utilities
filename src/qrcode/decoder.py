from PIL import Image
import pyzbar.pyzbar as pyzbar
import io
import sys
import os
import json

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from ui.decoder import Ui_MainWindow

os.chdir(os.path.dirname(__file__))
# Replace the working directory

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# Change the encoding of the console output

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file


def decodeQRcode(image: str):
    """
    QR code decoding
    Args:
        image: QR code image path
    Returns:
        QR code content
    """
    result = pyzbar.decode(Image.open(image), symbols=[pyzbar.ZBarSymbol.QRCODE])  # Parsing QR codes
    return result[0].data.decode("utf-8")


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect the buttons to the functions
        self.choosePictureButton.clicked.connect(self.choose_picture)
        self.decodeButton.clicked.connect(self.decode)
        self.filePath = ""

    def choose_picture(self):
        self.filePath = QFileDialog.getOpenFileName(self, "Select a QR code", "", "Image(*.png)")[0]
        if self.filePath:
            self.choosePictureButton.setText(self.filePath)

    def decode(self):
        if self.filePath != "":
            self.text = decodeQRcode(self.filePath)
            self.resultDisplay.setText(self.text)
        else:
            QMessageBox.critical(self, "Error", "Please select a QR code first.")


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
