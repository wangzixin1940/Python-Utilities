"""
Special Instructions:
The data for this program are from WWIS (World Weather Information Service, https://worldweather.wmo.int/).
"""

import requests
import csv
import traceback

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from ui.wr import Ui_MainWindow

import os
import json
import sys

os.chdir(os.path.dirname(__file__))
# Change the working directory to the current file's directory

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("./data/full_city_list.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    city_list = list(reader)
    # Read the city list file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["weather"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect the button to the function
        self.queryButton.clicked.connect(self.search_weather)
        # Bind events to the functions
        self.areaCodeEdit.editingFinished.connect(self.areaCodeChanged)
        self.countryEdit.editingFinished.connect(self.countryChanged)
        self.cityEdit.editingFinished.connect(self.cityChanged)
        self.countyEdit.editingFinished.connect(self.countyChanged)
        # Initialize the variables
        self.countries = []
        self.cities = []
        self.counties = []
        self.areaCode = 0
        self.anti_bug = True  # Used to prevent bugs, with no practical purpose.
        # Assign values to variables
        for line in city_list:
            self.countries.append(line[0])
            self.cities.append(line[1])
            if not line[2].isdigit():
                self.counties.append(line[2])

    def areaCodeChanged(self):
        for line in city_list:
            if line[2] == str(self.areaCodeEdit.value()):
                self.countryEdit.setText(line[0])
                self.cityEdit.setText(line[1])
                self.countyEdit.setText("<No data>")
                self.areaCode = self.areaCodeEdit.value()
                return
            elif line[3] == str(self.areaCodeEdit.value()):
                self.countryEdit.setText(line[0])
                self.cityEdit.setText(line[1])
                self.countyEdit.setText(line[2])
                self.areaCode = self.areaCodeEdit.value()
                return
        if self.areaCodeEdit.value() == 0 and self.anti_bug:
            self.anti_bug = False
            return
        QMessageBox.warning(self, "Warning", "No such area code found!")

    def countryChanged(self):
        if self.countryEdit.text() not in self.countries:
            QMessageBox.warning(self, "Warning", "No such country found!")
            self.countryEdit.clear()
        else:
            if self.countryEdit.text() not in ["Canada", "Colombia", "France",
                                               "Malta", "Philippines", "United States of America"]:
                self.countyEdit.setText("<No data>")
        if self.countryEdit.text() != self.cityEdit.text() != self.countyEdit.text() != "":
            id = 0
            for i in city_list:
                if self.countryEdit.text() == i[0] and self.cityEdit.text() == i[1]:
                    if not (i[2].isdigit()) and i[2] == self.countyEdit.text():
                        id = i[3]
                    else:
                        id = i[2]
                    break
            self.areaCodeEdit.setValue(id)

    def cityChanged(self):
        if self.cityEdit.text() not in self.cities:
            QMessageBox.warning(self, "Warning", "No such city found!")
            self.cityEdit.clear()
        else:
            if self.countryEdit.text() != "":
                if self.countryEdit.text() not in ["Canada", "Colombia", "France",
                                                   "Malta", "Philippines", "United States of America"]:
                    self.countyEdit.setText("<No data>")
        if self.countryEdit.text() != self.cityEdit.text() != self.countyEdit.text() != "":
            id = 0
            for i in city_list:
                if self.countryEdit.text() == i[0] and self.cityEdit.text() == i[1]:
                    if not (i[2].isdigit()) and i[2] == self.countyEdit.text():
                        id = i[3]
                    else:
                        id = i[2]
                    break
            self.areaCodeEdit.setValue(int(id))

    def countyChanged(self):
        if self.countyEdit.text() not in self.counties:
            QMessageBox.warning(self, "Warning", "No such county found!")
            self.countyEdit.clear()
        if self.countryEdit.text() != self.cityEdit.text() != self.countyEdit.text() != "":
            id = 0
            for i in city_list:
                if self.countryEdit.text() == i[0] and self.cityEdit.text() == i[1]:
                    if not (i[2].isdigit()) and i[2] == self.countyEdit.text():
                        id = i[3]
                    else:
                        id = i[2]
                    break
            self.areaCodeEdit.setValue(id)

    def search_weather(self):
        country = self.countryEdit.text()
        city = self.cityEdit.text()
        county = self.countyEdit.text()
        for i in city_list:
            if country == i[0] and city == i[1]:
                if not (i[2].isdigit()) and i[2] == county:
                    id = i[3]
                else:
                    id = i[2]
                break
        else:
            QMessageBox.critical(self, "Error", "No such city found!")
            return
        try:
            content = requests.get(f"https://worldweather.wmo.int/en/json/{id}_en.json")
            json_data = content.content.decode("utf-8")
            data = json.loads(json_data)
            # noinspection PyStringFormat
            text = f"""
{ui["infos"]["weather"]}
{ui["infos"]["forecastForDay2"]}
{ui["infos"]["forecastForDay3"]}
{ui["infos"]["forecastForDay4"]}
{ui["infos"]["forecastForDay5"]}
{ui["infos"]["forecastForDay6"]}
""".format(
                city=self.cityEdit.text(),
                tomorrow=data["city"]["forecast"]["forecastDay"][0]["weather"],
                dat=data["city"]["forecast"]["forecastDay"][1]["weather"],
                day4=data["city"]["forecast"]["forecastDay"][2]["forecastDate"],
                day4f=data["city"]["forecast"]["forecastDay"][2]["weather"],
                day5=data["city"]["forecast"]["forecastDay"][3]["forecastDate"],
                day5f=data["city"]["forecast"]["forecastDay"][3]["weather"],
                day6=data["city"]["forecast"]["forecastDay"][4]["forecastDate"],
                day6f=data["city"]["forecast"]["forecastDay"][4]["weather"],
            )
            QMessageBox.information(self, "Complete", text)
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, ui_src["error"], ui["infos"]["errorNetwork"] + "\n" + traceback.format_exc())
            return
        except:
            QMessageBox.critical(self, ui_src["error"], ui["infos"]["unknownError"] + "\n" + traceback.format_exc())
            return


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
