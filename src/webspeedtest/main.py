import datetime
import io
import json
import logging
import os
import sys

import speedtest

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator

from ui.st import Ui_MainWindow

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
# Change sys.stdout encoding to utf-8

os.chdir(os.path.dirname(__file__))
# Change working directory to the directory of the script

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["speedtest"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]

if not (settings["no-log-file"]):
    logging.basicConfig(
        filename=f"../../logs/{datetime.date.today()}.log",
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
logger = logging.getLogger("SPEEDTEST")


def webSpeedTest():
    logger.info("Prepare for the test")
    tester = speedtest.Speedtest()
    tester.get_servers()
    # theBest = tester.get_best_server()
    logger.info("Start testing")
    # 下载速度
    download_speed = int(tester.download() / 1024 / 1024)
    # 上传速度
    upload_speed = int(tester.upload() / 1024 / 1024)
    logger.info(
        f"Download Speed:{download_speed} MB; Upload Speed:{upload_speed} MB")
    return (download_speed, upload_speed)


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect the button to the function
        self.testButton.clicked.connect(self.test_speed)

    def test_speed(self):
        result = webSpeedTest()
        self.uploadSpeed.display(result[0])
        self.downloadSpeed.display(result[1])


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
