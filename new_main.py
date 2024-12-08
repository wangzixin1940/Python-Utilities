from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from data.ui import ui
import sys
import platform

import os
import json

with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

import io
import sys
import logging, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the standard output


os.chdir(os.path.dirname(__file__))
# Change the working directory to the directory of the script

with open(settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)  # type: dict[str: dict]

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
            "version": platform.python_version_tuple(),
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
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

def main():
    if check_python() != 0:
        sys.exit(-1)
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
