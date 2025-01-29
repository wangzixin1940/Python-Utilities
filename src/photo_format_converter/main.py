from PIL import Image
import os
import json
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QMessageBox, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from ui.pfc import Ui_MainWindow
import sys

os.chdir(os.path.dirname(__file__))
# Change the working directory to the current file's directory

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["photoFormatConverter"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect the buttons to the functions
        self.choosePhotoButton.clicked.connect(self.open_file)
        self.convertButton.clicked.connect(self.convert)

    def open_file(self):
        self.filePath = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.jpg *.png *.gif *.bmp)")[0]

    def convert(self):
        if self.filePath == "":
            QMessageBox.critical(self, "Error", "No picture selected!")
        else:
            image = Image.open(self.filePath)
            output = QFileDialog.getSaveFileName(self, "Save Image", "", "Image (*.{})".format(
                self.convertOptions.currentText().lower()))[0]
            if output:
                image.save(output)
                QMessageBox.information(self, "Information", "Conversion complete!")


if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    translator = QTranslator()
    if (translator.load(settings["qt_language"], directory="../../data/ui/i18n")):
        app.installTranslator(translator)
    window = App()
    window.setWindowIcon(QIcon("./assets/favicon.ico"))
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec())
