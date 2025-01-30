import os
import json

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from ui.smfj import Ui_MainWindow
import sys

from email.header import Header
from email.mime.text import MIMEText
import smtplib

import traceback

os.chdir(os.path.dirname(__file__))
# 更换工作目录

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["smfj"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


class Send:
    def __init__(self, json_file):
        super().__init__()
        self.json_file = json_file
        with open(self.json_file, "r", encoding="utf-8") as f:
            self.data = eval(repr(json.load(f)))  # type: dict
        self._from = {
            "email": self.data["from"],
            "pwd": self.data["password"],
            "name": self.data["name"]
        }
        if (self.data["encryption"] == "ssl"):
            self.smtp_obj = smtplib.SMTP_SSL(
                self.data["smtp_server"],
                self.data["smtp_port"],
                timeout=self.data["timeout"])
        elif (self.data["encryption"] == "tls") or (self.data["encryption"] == "starttls"):
            self.smtp_obj = smtplib.SMTP(
                self.data["smtp_server"],
                self.data["smtp_port"],
                timeout=self.data["timeout"])
            self.smtp_obj.starttls()
        elif (self.data["encryption"] is None):
            self.smtp_obj = smtplib.SMTP(
                self.data["smtp_server"],
                self.data["smtp_port"],
                timeout=self.data["timeout"])
        else:
            raise Exception("Encryption type not supported")
        self.recipients = self.data["emails"]
        self.smtp_obj.login(self._from["email"], self._from["pwd"])
        for recipient in self.recipients:
            self.message = MIMEText(recipient["body"], "plain", "utf-8")
            self.message["From"] = Header(self._from["name"], "utf-8")
            self.message["To"] = recipient["to"]
            self.message["Subject"] = Header(recipient["subject"], "utf-8")
            self.smtp_obj.sendmail(
                from_addr=self._from["email"],
                to_addrs=recipient["to"],
                msg=self.message.as_string())
        self.smtp_obj.quit()


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect the buttons to the functions
        self.chooseProfileButton.clicked.connect(self.chooseProfile)
        self.sendMailButton.clicked.connect(self.sendMail)

    def chooseProfile(self):
        self.profile = QFileDialog.getOpenFileName(self, "Choose a JSON profile", "", "JSON Files (*.json)")[0]

    def sendMail(self):
        if self.profile:
            try:
                Send(self.profile)
                QMessageBox.information(self, "Success", "Mail sent successfully")
            except smtplib.SMTPException:
                QMessageBox.critical(self, "Error", "A SMTP exception occurred:\n" + traceback.format_exc())
            except Exception:
                QMessageBox.critical(self, "Error", "An exception occurred:\n" + traceback.format_exc())
        else:
            QMessageBox.critical(self, "Error", "Please choose a profile first!")


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
