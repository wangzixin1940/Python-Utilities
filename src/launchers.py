import json


with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the standard output

with open(settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)  # type: dict[str: dict]

import logging, datetime
import threading
import os
from PySide6.QtWidgets import QMessageBox, QFileDialog, QApplication, QStyleFactory, QInputDialog, QLineEdit
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon
import subprocess

import src.devtools as DevTools

logging.basicConfig(
        filename=f"./logs/{datetime.date.today()}.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("DEVTOOLS")

app = QApplication.instance()
if app is None:
    app = QApplication([])
app.setStyle(QStyleFactory.create("Fusion"))
app.setWindowIcon(QIcon("./images/pride.ico"))
translator = QTranslator()
if (translator.load(settings["qt_language"], directory="./data/ui/i18n")):
    app.installTranslator(translator)

class DevToolsLauncher():

    def __init__(self):
        QMessageBox.critical(None, ui["error"], ui["invocationError"])
        logger.error("Invocation error")

    @staticmethod
    def webConnectTestLauncher():
        url = QInputDialog.getText(None, ui["launchers"]["dev"]["webConnectTest"]["input_url"], ui["launchers"]["dev"]["webConnectTest"]["input_url"], QLineEdit.Normal)[0]
        logger.info(f"User input: {url}")
        if url is not None:
            global DevTools
            result = DevTools.webConnectTest(url)
            error_list = ui["launchers"]["dev"]["error_list"]
            QMessageBox.information(None, "Python Utilities", error_list[str(result)])
            if not (1 == result or 2 == result):
                logger.info(f"Web address connect info: {url} => {result}")
                QMessageBox.information(None, "Python Utilities", result)
            else:
                QMessageBox.information(None, "Python Utilities", error_list[result - 1])

    @staticmethod
    def translatorLauncher():
        try:
            with open("data/translator.appid.json", "r") as appid:
                appid = appid.read()
                appid = json.loads(appid)
                id = appid["id"]
                key = appid["key"]
            entered = True
        except (FileNotFoundError, KeyError) as err:
            logger.error(repr(err))
            result = QMessageBox.question(None, ui["launchers"]["dev"]["translator"]["title"], ui["launchers"]["dev"]["translator"]["informationRequired"])
            if result == QMessageBox.StandardButton.Yes:
                data = QInputDialog.getMultiLineText(None, ui["launchers"]["dev"]["translator"]["title"], ui["launchers"]["dev"]["translator"]["informationInputs"]["message"], "\n".join(ui["launchers"]["dev"]["translator"]["informationInputs"]["fields"]))[0].split("\n")
                if data != None:
                    id = data[0]
                    key = data[1]
                    entered = True
                    with open("data/translator.appid.json", "w") as appid:
                        appid.write(json.dumps({"id": id, "key": key}))
                else:
                    entered = False
            else:
                entered = False
        if (entered):
            with open("./data/translator.languages.json", "r", encoding="utf-8") as languages:
                languages = languages.read()
                languages = json.loads(languages) # type: dict
            global DevTools
            text = QInputDialog.getText(None, ui["launchers"]["dev"]["translator"]["title"], ui["launchers"]["dev"]["translator"]["inputs"]["text"], QLineEdit.Normal)[0]
            if text:
                fromLang = "auto"
                toLang = QInputDialog.getItem(None, ui["launchers"]["dev"]["translator"]["title"], ui["launchers"]["dev"]["translator"]["inputs"]["languageChooseMessage"], list(languages.keys()), 0, True)
                logger.info(
                    f"User input:[{text}, {fromLang}, {languages[toLang[0]]}]")
                if (text != None) and (fromLang != None) and (toLang[0] != None):
                    result = DevTools.translator(
                        text, id, key, fromLang, languages[toLang[0]])
                    QMessageBox.information(None, ui["launchers"]["dev"]["translator"]["title"],
                                            f"{ui["launchers"]["dev"]["translator"]["completeInformation"]["complete"]}\n \
{ui["launchers"]["dev"]["translator"]["completeInformation"]["original"]}{text}\n \
{ui["launchers"]["dev"]["translator"]["completeInformation"]["result"]} {result}\n \
{ui["launchers"]["dev"]["translator"]["completeInformation"]["language"]} {toLang[0]}")
                    logger.info(f"Result: {result}")
                else:
                    QMessageBox.critical(None, ui["launchers"]["dev"]["translator"]["title"], ui["launchers"]["dev"]["translator"]["errorInformationMessage"])
                    logger.error("Missing arguments")

    @staticmethod
    def JSONtoXMLLauncher():
        json = QFileDialog.getOpenFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["openTitle"], "", "JSON File(*.json)")[0]
        xml = QFileDialog.getSaveFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["saveTitle"], "", "XML File(*.xml)")[0]
        if (json != None):
            if (os.path.splitext(json)[-1] == ".json"):
                global DevTools
                logger.info(f"Input JSON:{json}")
                DevTools.JSONtoXML(json, xml)
                logger.info(f"Output finish")
            else:
                QMessageBox.critical(None, ui["error"], ui["launchers"]["dev"]["fileConverters"]["extensionError"])
                logger.error("File extension is incorrect")

    @staticmethod
    def XMLtoJSONLauncher():
        xml = QFileDialog.getOpenFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["openTitle"], "", "XML Files(*.xml)")[0]
        json = QFileDialog.getSaveFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["saveTitle"], "", "JSON File(*.json)")[0]
        if (xml != None):
            if (os.path.splitext(xml)[-1] == ".xml"):
                global DevTools
                logger.info(f"Input XML:{xml}")
                DevTools.XMLtoJSON(xml, json)
                logger.info(f"Output finish")
            else:
                QMessageBox.critical(None, ui["error"], ui["launchers"]["dev"]["fileConverters"]["extensionError"])
                logger.error("File extension is incorrect")

    @staticmethod
    def getIPLauncher():
        global DevTools
        ip = QInputDialog.getText(None, ui["launchers"]["dev"]["socketTools"]["getIP"]["title"], ui["launchers"]["dev"]["socketTools"]["getIP"]["inputMessage"], QLineEdit.Normal)[0]
        if (ip != None):
            if (ip != "@default"):
                logger.info(f"Input IP:{ip}")
                result = DevTools.getIP(ip)
                QMessageBox.information(None, ui["launchers"]["dev"]["socketTools"]["getIP"]["title"], f"{ui["launchers"]["dev"]["socketTools"]["getIP"]["ip"]} {result}")
                logger.info(f"Result: {result}")
            else:
                logger.info(f"Input IP:{ip}")
                result = DevTools.getIP()
                QMessageBox.information(None, ui["launchers"]["dev"]["socketTools"]["getIP"]["title"], f"{ui["launchers"]["dev"]["socketTools"]["getIP"]["ip"]} {result}")
                logger.info(f"Result: {result}")

    @staticmethod
    def resolveDomainLauncher():
        domain = QInputDialog.getText(None, ui["launchers"]["dev"]["socketTools"]["resolveDomain"]["Domain"], ui["launchers"]["dev"]["socketTools"]["resolveDomain"]["input"], QLineEdit.Normal)[0]
        if (domain != None):
            global DevTools
            logger.info(f"Input Domain: {domain}")
            result = DevTools.resolveDomain(domain)
            QMessageBox.information(None, ui["launchers"]["dev"]["socketTools"]["resolveDomain"]["title"], f"{ui["launchers"]["dev"]["socketTools"]["resolveDomain"]["Domain"]} {result}")
            logger.info(f"Result: {result}")

    @staticmethod
    def JSONtoCSVLauncher():
        json = QFileDialog.getOpenFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["openTitle"], "", "JSON File(*.json)")[0]
        csv = QFileDialog.getSaveFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["saveTitle"], "", "CSV File(*.csv)")[0]
        if (json != None):
            if (os.path.splitext(json)[-1] == ".json"):
                global DevTools
                logger.info(f"Input JSON:{json}")
                DevTools.JSONtoCSV(json, csv)
                logger.info(f"Output finish")
            else:
                QMessageBox.critical(None, ui["error"], ui["launchers"]["dev"]["fileConverters"]["extensionError"])
                logger.error("File extension is incorrect")

    @staticmethod
    def CSVtoJSONLauncher():
        csv = QFileDialog.getOpenFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["openTitle"], "", "CSV File(*.csv)")[0]
        json = QFileDialog.getSaveFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["saveTitle"], "", "JSON File(*.json)")[0]
        
        if (csv != None):
            if (os.path.splitext(csv)[-1] == ".csv"):
                global DevTools
                logger.info(f"Input CSV:{csv}")
                DevTools.CSVtoJSON(csv, json)
                logger.info(f"Output finish")
            else:
                QMessageBox.critical(None, ui["error"], ui["launchers"]["dev"]["fileConverters"]["extensionError"])
                logger.error("File extension is incorrect")

class DrawingToolsLauncher():
    def __init__(self):
        QMessageBox.critical(None, ui["error"], ui["invocationError"])
        logger.error("Invocation error")

    @staticmethod
    def charPictureLauncher():
        path =  QFileDialog.getOpenFileName(None, ui["launchers"]["art"]["asciiArt"]["open"], "", "Image(*.png *.gif)")[0]
        if (path != None):
            if (os.path.splitext(path)[-1] == ".png") or (os.path.splitext(path)[-1] == ".jpg") or (
                    os.path.splitext(path)[-1] == ".bmp") or (os.path.splitext(path)[-1] == ".gif") or (
                    os.path.splitext(path)[-1] == ".jpeg"):
                global DrawingTools
                logger.info(f"Input picture:{path}")
                DrawingTools.charPicture(path)
            else:
                QMessageBox.critical(None, ui["error"], ui["launchers"]["art"]["asciiArt"]["extensionError"])
                logger.error("File extension is incorrect")

    @staticmethod
    def bingPictureLauncher():
        filename = QFileDialog.getSaveFileName(None, ui["launchers"]["art"]["bingPicture"]["saveAs"], "", "Image(*.jpg *.*)")[0]
        if (filename != None):
            logger.info(f"Input path: {filename}")
            if (os.path.splitext(filename)[-1] == ".jpg"):
                params = QInputDialog.getMultiLineText(None, ui["launchers"]["art"]["bingPicture"]["title"], ui["launchers"]["art"]["bingPicture"]["inputs"]["msg"], "\n".join(ui["launchers"]["art"]["bingPicture"]["inputs"]["fields"])).spilt("\n")
                if (params != None != ["", ""]):
                    if (params[0].isdigit()) or (params[0] == "-1"):
                        params.insert(0, filename)
                        logger.info(f"Input params:{params}")
                        global DrawingTools
                        DrawingTools.bingPicture(
                            params[0], params[1], params[2])
                        logger.info("Done.")
                        QMessageBox.information(None, ui["info"], ui["launchers"]["art"]["bingPicture"]["success"])
                    else:
                        QMessageBox.critical(None, ui["error"], ui["launchers"]["art"]["bingPicture"]["indexError"])
                        return
            else:
                logger.error("File extension is incorrect")
                QMessageBox.critical(None, ui["error"], ui["launchers"]["art"]["bingPicture"]["extensionError"])
                return

class ExternalLauncher():
    def __init__(self):
        QMessageBox.critical(None, ui["error"], ui["invocationError"])
        logger.error("Invocation error")

    @staticmethod
    def webSpeedTestLauncher():
        def run():
            subprocess.Popen("python /src/webspeedtest/main.py")
        QMessageBox.warning(None, ui["warn"], ui["launchers"]["external"]["webSpeedTestWarning"])
        thread = threading.Thread(target=run)
        thread.start()

    @staticmethod
    def clockLauncher():
        subprocess.Popen("python src/clock/main.py")

    @staticmethod
    def calculatorLauncher():
        subprocess.Popen("python src/calculator/main.py")

    @staticmethod
    def hashCheckerLauncher():
        QMessageBox.information(None, "Python Utilities", ui["launchers"]["external"]["hashCheckerWarning"])

    @staticmethod
    def passwordCreatorLauncher():
        subprocess.Popen("python src/passwordCreator/main.py")

    @staticmethod
    def licenceCreatorLauncher():
        subprocess.Popen("python src/licenceCreator/main.py")

    @staticmethod
    def qrcodeGeneratorLauncher():
        subprocess.Popen("python src/qrcode/main.py 0")

    @staticmethod
    def qrcodeParserLauncher():
        subprocess.Popen("python src/qrcode/main.py 1")

    @staticmethod
    def weatherLauncher():
        subprocess.Popen("python src/weather/main.py")

    @staticmethod
    def speech2textLauncher():
        subprocess.Popen("python src/speech2text/main.py")

    @staticmethod
    def pictureFormatConverterLauncher():
        subprocess.Popen("python src/photo_format_converter/main.py")

    @staticmethod
    def sendMailFromJSONLauncher():
        subprocess.Popen("python src/send_mail_from_json/main.py")

    @staticmethod
    def AMKLauncher():
        subprocess.Popen("python src/auto_mouse_and_keyboard/main.py")

    @staticmethod
    def countDownLauncher():
        subprocess.Popen("python src/count_down/main.py")

    @staticmethod
    def pinyinLauncher():
        subprocess.Popen("python src/Chinese_Pinyin_Dictionary/main.py")

    @staticmethod
    def captchaLauncher():
        subprocess.Popen("python src/Captcha_Generator/main.py")

    @staticmethod
    def toDoLauncher():
        subprocess.Popen("python src/EasyTodo/main.py")

