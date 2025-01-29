import json
import os
import sys

import pypinyin
from PySide6 import QtWidgets
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyleFactory

from ui.cpd import Ui_MainWindow

os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file


def query(word):
    """
    Query the pinyin of a Chinese character
    Args:
        word: Chinese character
    Returns:
        Pinyin
    """
    return (pypinyin.pinyin(word, style=pypinyin.TONE, v_to_u=True), pypinyin.pinyin(word, style=pypinyin.BOPOMOFO,
                                                                                     v_to_u=True))
    # Output pinyin and zhuyin, with tones, replace v with ü (ㄩ)


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Define the variables
        self.pinyin = ""
        self.zhuyin = ""
        self.text = ""
        # Connect the button to the function
        self.queryButton.clicked.connect(self.processing)

    def processing(self):
        self.text = self.inputs.text()
        result = query(self.text)
        self.pinyin = result[0][0][0] + " " + result[0][1][0]
        self.zhuyin = result[1][0][0] + " " + result[1][1][0]
        self.resultPinyin.setText(self.pinyin)
        self.resultZhuyin.setText(self.zhuyin)


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
