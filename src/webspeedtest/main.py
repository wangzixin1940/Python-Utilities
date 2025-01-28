from tkinter import scrolledtext
import ttkbootstrap as tkinter
import datetime
import logging
import speedtest
import io
import sys
import os
import json


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


"""root = tkinter.Window()
root.title(ui["title"])
root.geometry("350x350")
root.resizable(False, False)

txt = scrolledtext.ScrolledText(root, width=45, height=20)
txt.grid(column=0, row=0)

txt.pack()  # The title of the text box

txt.insert(
    tkinter.INSERT,
    ui["about"])
result = webSpeedTest()
txt.insert(tkinter.INSERT, ui["info"].format(up=result[0], down=result[1]))
txt.config(state=tkinter.DISABLED)

root.mainloop()"""

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMessageBox, QStyleFactory, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator

from ui.st import Ui_MainWindow


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
