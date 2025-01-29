from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMessageBox, QStyleFactory, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
import os
import io
import sys
import json

from ui.lc import Ui_MainWindow


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# 更换编码

os.chdir(os.path.dirname(__file__))
# 更换工作目录

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["licenceCreator"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]

with open("models/apache-v2.txt", "r", encoding="utf-8") as apache:
    apache_licence = apache.read()

with open("models/mit.txt", "r", encoding="utf-8") as mit:
    mit_licence = mit.read()

with open("models/gpl-v3.txt", "r", encoding="utf-8") as gpl:
    gpl_licence = gpl.read()

with open("models/isc.txt", "r", encoding="utf-8") as isc:
    isc_licence = isc.read()
# Import the licence templates


class LicenceCreator():
    def __init__(self, licence: str, params: dict):
        self.licence = licence
        if licence == "apache":
            self.make_apache_licence(params["name"], params["year"])
        elif licence == "mit":
            self.make_mit_licence(params["name"], params["year"])
        elif licence == "gpl":
            self.make_gpl_licence(
                params["name"],
                params["year"],
                params["usage"],
                params["project_name"])
        elif licence == "isc":
            self.make_isc_licence(params["name"], params["year"])
        else:
            raise self.LicenceNotFound("Licence not found: {}".format(licence))

    def make_apache_licence(self, name: str, year: int):
        self.name = name
        self.year = year
        self.licence = apache_licence.format(str(year), name)

    def make_mit_licence(self, name: str, year: int):
        self.name = name
        self.year = year
        self.licence = mit_licence.format(str(year), name)

    def make_gpl_licence(
            self,
            name: str,
            year: int,
            usage: str,
            project_name: str):
        self.name = name
        self.year = year
        self.usage = usage
        self.project_name = project_name
        self.licence = gpl_licence.format(usage, str(year), name, project_name)

    def make_isc_licence(self, name: str, year: int):
        self.name = name
        self.year = year
        self.licence = isc_licence.format(str(year), name)

    class LicenceNotFound(Exception):
        def __init__(self, message="Licence not found"):
            self.message = message
            super().__init__(self.message)


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Define the variables
        self.name = ""
        self.year = 0
        self.project_intro = ""
        self.project_name = ""
        self.type = -1
        self.licence_text = ""
        # Connect the button to the function
        self.generateButton.clicked.connect(self.generate_licence)
        # Change the maximum value of the Spinbox
        self.yearEdit.setMaximum(9999)
        self.yearEdit_2.setMaximum(9999)
        self.yearEdit_3.setMaximum(9999)
        self.yearEdit_4.setMaximum(9999)

    def generate_licence(self):
        self.tab = self.types.currentIndex()
        match self.tab:
            case 0:  # Apache 2.0
                self.name = self.nameEdit.text()
                self.year = self.yearEdit.text()
                self.licence_text = LicenceCreator("apache", {"name": self.name, "year": self.year}).licence
            case 1:  # MIT
                self.name = self.nameEdit_2.text()
                self.year = self.yearEdit_2.text()
                self.licence_text = LicenceCreator("mit", {"name": self.name, "year": self.year}).licence
            case 2:  # GPL v3
                self.name = self.nameEdit_3.text()
                self.year = self.yearEdit_3.text()
                self.project_intro = self.projectIntroEdit.text()
                self.project_name = self.projectNameEdit.text()
                self.licence_text = LicenceCreator("gpl", {"name": self.name, "year": self.year,
                                                           "usage": self.project_intro,
                                                           "project_name": self.project_name}).licence
            case 3:  # ISC
                self.name = self.nameEdit_4.text()
                self.year = self.yearEdit_4.text()
                self.licence_text = LicenceCreator("isc", {"name": self.name, "year": self.year}).licence
            case _:  # Error
                QMessageBox.critical(self, "Error", "An unknown error occurred.")
        self.path = QFileDialog.getSaveFileName(self, "Save the licence", "", "Text files (*.txt);;All files (*)")
        with open(self.path[0], "w", encoding="utf-8") as file:
            file.write(self.licence_text)
        QMessageBox.information(self, "Complete", "The licence has been saved successfully.")


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
