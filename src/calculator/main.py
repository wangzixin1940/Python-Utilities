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
    ui = json.loads(ui_src_file)["externals"]["calculator"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


import math
import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMessageBox, QStyleFactory
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from ui.calc import Ui_MainWindow

import traceback


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./images/pride.ico"))
        # Define the signs
        self.signs_group = ["%", "^", "2√", "/", "*", "-", "+"]
        self.functions_group = ["CE", "C", "±", "="]
        # Define the datas
        self.data = []
        self.previous_type = "number"
        # Connect the buttons to the function
        self.button_0.clicked.connect(lambda: self.button_click("0"))
        self.button_00.clicked.connect(lambda: self.button_click("00"))
        self.button_1.clicked.connect(lambda: self.button_click("1"))
        self.button_2.clicked.connect(lambda: self.button_click("2"))
        self.button_3.clicked.connect(lambda: self.button_click("3"))
        self.button_4.clicked.connect(lambda: self.button_click("4"))
        self.button_5.clicked.connect(lambda: self.button_click("5"))
        self.button_6.clicked.connect(lambda: self.button_click("6"))
        self.button_7.clicked.connect(lambda: self.button_click("7"))
        self.button_8.clicked.connect(lambda: self.button_click("8"))
        self.button_9.clicked.connect(lambda: self.button_click("9"))
        self.button_dot.clicked.connect(lambda: self.button_click("."))
        self.button_add.clicked.connect(lambda: self.button_click("+"))
        self.button_sub.clicked.connect(lambda: self.button_click("-"))
        self.button_mul.clicked.connect(lambda: self.button_click("*"))
        self.button_div.clicked.connect(lambda: self.button_click("/"))
        self.button_equ.clicked.connect(lambda: self.button_click("="))
        self.button_ce.clicked.connect(lambda: self.button_click("CE"))
        self.button_c.clicked.connect(lambda: self.button_click("C"))
        self.button_per.clicked.connect(lambda: self.button_click("%"))
        self.button_pn.clicked.connect(lambda: self.button_click("±"))
        self.button_clo.clicked.connect(lambda: self.button_click("^"))
        self.button_root.clicked.connect(lambda: self.button_click("2√"))

    def button_click(self, text: str):
        if (text in self.functions_group):  # 功能
            match text:
                case "CE":
                    self.data.remove(self.data[-1])
                    self.result.display(self.data[-1])
                case "C":
                    self.data = []
                    self.result.display(0)
                case "±":
                    if self.data[-1] in self.signs_group:
                        QMessageBox.critical(self, ui_src["error"], ui["positivityError"])
                        self.result.display(0)
                    else:
                        self.data[-1] = str(-float(self.data[-1]))
                        self.result.display(self.data[-1])
                case "=":
                    try:
                        self.data = [str(eval("".join(self.data)))]
                        self.result.display(self.data[-1])
                    except ZeroDivisionError:
                        QMessageBox.critical(self, ui_src["error"], ui["divideByZeroError"])
                        self.data = []
                        self.result.display(0)
                    except ValueError:
                        QMessageBox.critical(self, ui_src["error"], ui["overflowError"].format(max=str(sys.get_int_max_str_digits()) + "**10 - 1"))
                        self.data = []
                        self.result.display(0)
                    except Exception as err:
                        QMessageBox.critical(self, ui_src["error"], traceback.format_exc())
                        self.data = []
                        self.result.display(0)
            self.previous_type = "function"
        elif (text in self.signs_group):  # 符号
            match text:
                case "%":
                    self.data[-1] = str(float(self.data[-1]) / 100)
                    self.result.display(self.data[-1])
                case "^":
                    self.data.append("**")
                case "2√":
                    self.data[-1] = str(math.sqrt(float(self.data[-1])))
                    self.result.display(self.data[-1])
                case _:
                    self.data.append(text)
            self.previous_type = "sign"
        else:  # 数字
            if (self.previous_type == "number"):
                if not self.data == []:
                    self.data[-1] = self.data[-1] + text
                else:
                    self.data.append(text)
            else:
                self.data.append(text)
            self.result.display(self.data[-1])
            self.previous_type = "number"

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    translator = QTranslator()
    if (translator.load(settings["qt_language"], directory="./data/ui/i18n")):
        app.installTranslator(translator)
    window = App()
    window.setWindowIcon(QIcon("./images/pride.ico"))
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec())
