from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from data.ui import main_ui
from data.ui import about
import platform

import os
import json

import src.launchers as launchers
import shutil

with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

import io
import sys
import logging
import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the standard output


os.chdir(os.path.dirname(__file__))
# Change the working directory to the directory of the script

with open(settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = json.loads(ui_src_file.read())  # type: dict[str: dict]
    file_types = ui_src_file["filetypes"]  # type: dict[str: list[str]]

if not (settings["no-log-file"]):
    logging.basicConfig(
        filename=f"logs/{datetime.date.today()}.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - NO-LOG-FILE - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
logger = logging.getLogger("ROOT")
# Configure the logger


def check_python():
    global sysinfo
    sysinfo = {
        "system": platform.system(),
        "version": platform.version(),
        "python": {
            "version": list(platform.python_version_tuple()),
            "implementation": platform.python_implementation(),
        }
    }
    for i in range(len(sysinfo["python"]["version"])):
        if not ("b" in str(sysinfo["python"]["version"][i])):
            sysinfo["python"]["version"][i] = int(sysinfo["python"]["version"][i])
        else:
            sysinfo["python"]["version"][i] = sysinfo["python"]["version"][i].split("b")[
                0]
    logger.info("Platform: {system} {version}".format(
        system=sysinfo["system"], version=sysinfo["version"]))
    logger.info("Python: {version} {implementation}".format(version=sysinfo["python"]["version"],
                                                            implementation=sysinfo["python"]["implementation"]))
    # Outputs system information
    if sysinfo["python"]["version"][0] >= 3:
        if sysinfo["python"]["version"][1] >= 10:
            logger.info("Successfully attempted to start the main function.")
            return 0
        else:
            logger.warning("Python version too old: {}".format(
                sysinfo["python"]["version"]))
    else:
        logger.warning("Python version too old: {}".format(
            sysinfo["python"]["version"]))
    logger.critical("Python version TOO OLD !!! Program CANNOT LAUNCH!!!")
    return 1


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = main_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons to functions
        self.ui.import_settings.triggered.connect(self.import_settings)
        self.ui.exit.triggered.connect(self.close)
        self.ui.about.triggered.connect(self.about_window)
        self.ui.choose_language_profile.triggered.connect(self.choose_language_profile)
        self.ui.translator.clicked.connect(launchers.DevToolsLauncher.translatorLauncher)
        self.ui.weather_report.clicked.connect(launchers.ExternalLauncher.weatherLauncher)
        self.ui.speech_to_text.clicked.connect(launchers.ExternalLauncher.speech2textLauncher)
        self.ui.easy_to_do.clicked.connect(launchers.ExternalLauncher.toDoLauncher)
        self.ui.password_creator.clicked.connect(launchers.ExternalLauncher.passwordCreatorLauncher)
        self.ui.calculator.clicked.connect(launchers.ExternalLauncher.calculatorLauncher)
        self.ui.hash_checker.clicked.connect(launchers.ExternalLauncher.hashCheckerLauncher)
        self.ui.licence_creator.clicked.connect(launchers.ExternalLauncher.licenceCreatorLauncher)
        self.ui.send_mail_from_json.clicked.connect(launchers.ExternalLauncher.sendMailFromJSONLauncher)
        self.ui.get_ip.clicked.connect(launchers.DevToolsLauncher.getIPLauncher)
        self.ui.get_doamin.clicked.connect(launchers.DevToolsLauncher.resolveDomainLauncher)
        self.ui.create_qr.clicked.connect(launchers.ExternalLauncher.qrcodeGeneratorLauncher)
        self.ui.reslove_qr.clicked.connect(launchers.ExternalLauncher.qrcodeParserLauncher)
        self.ui.json_to_csv.clicked.connect(launchers.DevToolsLauncher.JSONtoCSVLauncher)
        self.ui.json_to_xml.clicked.connect(launchers.DevToolsLauncher.JSONtoXMLLauncher)
        self.ui.xml_to_json.clicked.connect(launchers.DevToolsLauncher.XMLtoJSONLauncher)
        self.ui.csv_to_json.clicked.connect(launchers.DevToolsLauncher.CSVtoJSONLauncher)
        self.ui.amk_app.clicked.connect(launchers.ExternalLauncher.AMKLauncher)
        self.ui.captcha_generator.clicked.connect(launchers.ExternalLauncher.captchaLauncher)
    
    def choose_language_profile(self):
        language_profile = QtWidgets.QFileDialog.getOpenFileName(self, "Choose Language Profile (JSON)", "",
                                                                 "JSON Files (*.json)")[0]
        if language_profile != "":
            qt_language_profile = QtWidgets.QFileDialog.getOpenFileName(self, "Choose Language Profile (QM)", "",
                                                                        "Qt Released Language Files (*.qm)")
            if qt_language_profile != "":
                with open("./data/settings.json", "r+", encoding="utf-8") as settings:
                    settings_data = json.loads(settings)
                    settings_data["language"] = language_profile
                    settings_data["qt_language"] = qt_language_profile
                    json.dump(settings_data, settings, indent=4, ensure_ascii=False)
    
    def import_settings(self):
        settings = QtWidgets.QFileDialog.getOpenFileName(self, "Choose Settings File (JSON)", "",
                                                         "JSON Files (*.json)")[0]
        if settings != "":
            response = QtWidgets.QMessageBox.question(self, "Warning",
                                                      "Are you sure you want to import the settings file?\n \
                                                      This will overwrite the current settings file!",
                                                      QtWidgets.QMessageBox.StandardButton.Yes,
                                                      QtWidgets.QMessageBox.StandardButton.No)
            if response == QtWidgets.QMessageBox.StandardButton.Yes:
                os.remove("./data/settings.json")
                shutil.copy(settings, "./data/settings.json")
                QtWidgets.QMessageBox.information(self, "Success",
                                                  "Successfully replaced the settings file!\n \
                                                  Restart the program to apply the changes.",
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
    
    @ staticmethod
    def about_window():
        about_window = AboutWindow()
        about_window.show()
        return about_window.exec()
            

class AboutWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.ui = about.Ui_Dialog()
        self.ui.setupUi(self)


def main():
    if check_python() != 0:
        sys.exit(-1)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    translator = QTranslator()
    if (translator.load(settings["qt_language"], directory="./data/ui/i18n")):
        app.installTranslator(translator)
    window = MainWindow()
    window.setWindowIcon(QIcon("./images/pride.ico"))
    window.resize(320, 500)
    window.setFixedSize(320, 500)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
