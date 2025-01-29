import qrcode
from qrcode.image.styledpil import StyledPilImage
import json
import io
import sys
import os

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from ui.generator import Ui_MainWindow

# noinspection PyUnresolvedReferences
from qrcode.image.styles.moduledrawers import *
# noinspection PyUnresolvedReferences
from qrcode.image.styles.colormasks import *

import traceback

os.chdir(os.path.dirname(__file__))
# Change the working directory to the current file's directory

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# Change the encoding of the standard output to the encoding specified in the settings file


def generateQRcode(
        data: str,
        filename: str,
        module_drawer=None,
        color_mask=None,
        embedded_image_path: str | None = None,
        *args):
    """
    Generate a QR code
    Args:
        data: QR code data
        filename: Save the file name of the QR code
        module_drawer: Drawer
        color_mask: Color mask
        embedded_image_path: Embedded image path
    """
    qr = qrcode.main.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    qr.add_data(data)
    qr.make(data)
    if embedded_image_path and module_drawer and color_mask:
        img = qr.make_image(
            *args,
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask,
            embeded_image=embedded_image_path)
    elif embedded_image_path and module_drawer:
        img = qr.make_image(
            *args,
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            embeded_image=embedded_image_path)
    elif embedded_image_path and color_mask:
        img = qr.make_image(
            *args,
            image_factory=StyledPilImage,
            color_mask=color_mask,
            embeded_image=embedded_image_path)
    elif module_drawer and color_mask:
        img = qr.make_image(
            *args,
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask)
    elif module_drawer:
        img = qr.make_image(
            *args,
            image_factory=StyledPilImage,
            module_drawer=module_drawer)
    elif color_mask:
        img = qr.make_image(
            *args,
            image_factory=StyledPilImage,
            color_mask=color_mask)
    elif embedded_image_path:
        img = qr.make_image(
            *args,
            image_factory=StyledPilImage,
            embeded_image=embedded_image_path)
    else:
        img = qr.make_image(*args, image_factory=StyledPilImage)
    img.save(filename)


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect the buttons to the functions
        self.generateButton.clicked.connect(self.generate)
        self.pictureChooseButton.clicked.connect(self.choose_picture)
        # Define the variables
        self.chose_image = False
        self.drawer = None
        self.colorMask = None
        self.filePath = ""
        self.savePath = ""

    def generate(self):
        self.text = self.textEdit.toPlainText()
        self.drawer = self.drawerChooseBox.currentText()
        self.colorMask = self.colorMaskChooseBox.currentText()
        self.savePath = QFileDialog.getSaveFileName(self, "Save as", "", "Image(*.png)")[0]
        if self.savePath:
            try:
                if self.chose_image:
                    generateQRcode(
                        self.text, self.savePath,
                        eval(self.drawer + "()"),
                        eval(self.colorMask + "()"), self.filePath)
                else:
                    generateQRcode(
                        self.text, self.savePath,
                        eval(self.drawer + "()"),
                        eval(self.colorMask + "()"), None)
                QMessageBox.information(self, "Success", "QR code generated successfully")
            except:
                QMessageBox.critical(self, "Error", "Failed to generate QR code:\n" + traceback.format_exc())

    def choose_picture(self):
        self.filePath = QFileDialog.getOpenFileName(self, "Select an image", "", "Image(*.png)")[0]
        if self.filePath:
            self.pictureChooseButton.setText(self.filePath)
            self.chose_image = True


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
