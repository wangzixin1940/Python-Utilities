import io
import json
import os
import random
import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from ui.pc import Ui_MainWindow

import pyperclip as cb

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
# Change the encoding of the console output to utf-8

os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["passwordCreator"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


def passwordCreator(
        length: int,
        includeSymbols: bool = False,
        includeNumbers: bool = True,
        includeUppercase: bool = True):
    """
    Generate passwords
    Args:
        length: Password length
        includeSymbols: Whether to include symbols
        includeNumbers: Whether to include numbers
        includeUppercase: Whether to include capital letters
    Returns:
        Password string
    """
    # Password character set
    chars = {
        "lowers": "abcdefghijklmnopqrstuvwxyz",
        "uppers": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "numbers": "0123456789",
        "symbols": "!#$%&*+-?@^_|~"
    }
    if not includeSymbols:
        del chars["symbols"]
    if not includeNumbers:
        del chars["numbers"]
    if not includeUppercase:
        del chars["uppers"]
    password = ""
    try:
        for i in range(int(length)):
            # A character set is selected at random
            charset = random.choice(list(chars.keys()))
            # Choose a character at random
            char = random.choice(chars[charset])
            # Add to the password string
            password += char
        return password
    except Exception:
        return 1


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect the buttons to the functions
        self.generateButton.clicked.connect(self.generate)
        self.copyButton.clicked.connect(self.copy)

    def copy(self):
        if self.passwordDisplay.text() == "":
            QMessageBox.critical(self, "Error", "No password to copy!")
        else:
            cb.copy(self.passwordDisplay.text())
            QMessageBox.information(self, ui["copied"], ui["completeInformation"])

    def generate(self):
        self.length = self.digitsInput.value()
        self.includeUppersChoice = self.includeUppers.isChecked()
        self.includeNumbersChoice = self.includeNumbers.isChecked()
        self.includeSymbolsChoice = self.includeSymbols.isChecked()
        self.password = passwordCreator(
            self.length, self.includeSymbolsChoice, self.includeNumbersChoice, self.includeUppersChoice
        )
        self.passwordDisplay.setText(self.password)


if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    translator = QTranslator()
    if (translator.load(settings["qt_language"], directory="../../data/ui/i18n")):
        app.installTranslator(translator)
    window = App()
    window.setWindowIcon(QIcon("./assets/icon.ico"))
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec())
