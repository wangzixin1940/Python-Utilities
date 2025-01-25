import os
import json
os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

import traceback
import pynput
from pynput import mouse
from pynput import keyboard
from time import sleep as delay
from random import randint as rand


class Controllers:
    def __init__(self):
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()


class Functions:
    def __init__(self):
        self.mouse = pynput.mouse
        self.keybrd = pynput.keyboard

    @staticmethod
    def delay(*args, **kwargs):
        return delay(*args, **kwargs)

    @staticmethod
    def rand(*args, **kwargs):
        return rand(*args, **kwargs)


Controllers = Controllers()
Functions = Functions()

# 可用的方法：mouse, keyboard, delay, rand

# mouse, keybrd 语法见 https://pynput.readthedocs.io/en/latest/index.html

# delay 语法：
# delay(sec: int)
# 等待 sec 秒

# rand 语法：
# rand(min: int, max: int)
# 在 min 到 max 之间随机取一个数

mouse = mouse.Controller()
keyboard = keyboard.Controller()


from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QMessageBox, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
import sys


from ui.amk import Ui_Dialog

class App(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        # Connect the buttons to their respective functions
        self.choose_file.clicked.connect(self.choose_file_work)
        self.run_script.clicked.connect(self.run_script_work)
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.helpRequested.connect(lambda: QMessageBox.information(self, "Help", "This app can automatically manage your mouse and keyboard actions with just a simple macro."))

    def choose_file_work(self):
        self.file = QFileDialog.getOpenFileName(self, "Open File", "", "AMK Script(*.amk);Python Script(*.py);All Files(*)")[0]
        if self.file:
            self.choose_file.setText(self.file)
        return 0
    
    def run_script_work(self):
        if self.file:
            try:
                exec(open(self.file).read())
            except Exception as e:
                QMessageBox.critical(self, "Error", traceback.format_exc())
        return 0

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
