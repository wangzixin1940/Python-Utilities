import json
import logging
import datetime
import threading
import os
from PySide6.QtWidgets import QMessageBox, QFileDialog, QApplication, QStyleFactory, QInputDialog
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon
import subprocess
import random
import hashlib
import urllib
import http
import dicttoxml
import xmltodict
import socket
from difflib import HtmlDiff
import requests
import io
import sys
from PIL import Image


with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the standard output

with open(settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)  # type: dict[str: dict]

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


class DevTools:
    def webConnectTest(url: str):  # TODO: 添加功能到主UI
        """
        Test if the website is accessible
        Args:
            url: Website URL
        Returns:
            Status code or connection result
        """
        try:
            result = str(requests.get(url).status_code)
        except requests.exceptions.MissingSchema:
            logger.critical("Missing schema error")
            return 1
        # Return HTTP status code
        with open("./data/connect.test.codes.json", "r") as status_codes:
            status_codes = status_codes.read()
            status_codes = json.loads(status_codes)
        # A list of common HTTP status codes
        try:
            return str(result) + " : " + status_codes[result]
        except KeyError:
            logger.error(f"Status code: {result} not found")
            return 2
        # If the HTTP status code is known, the result is returned.
        # Otherwise, the user is prompted to return an unknown status code

    def translator(text: str, appid: str, secret_key: str, original_language: str, target_language: str):
        """
        Translate text with Baidu Translate
        Args:
            text: Texts that need to be translated
            appid: The AppID of Baidu Translate API
            secret_key: The Secret Key of Baidu Translate API
            original_language: Original language
            target_language: Translation language
        Returns
            Translation result or null value Zero (error)
        """

        class fake_http_client_http_connection:
            def __init__(self, *args, **kwargs):
                pass

            def close(self, *args, **kwargs):
                pass

        trans_result = None
        salt = random.randint(32768, 65536)
        sign = hashlib.md5((str(appid) + text + str(salt) +
                            secret_key).encode()).hexdigest()
        target_url = "https://api.fanyi.baidu.com/api/trans/vip/translate" + "?appid=" + str(
            appid) + "&q=" + urllib.parse.quote(
            text) + "&from=" + original_language + "&to=" + target_language + "&salt=" + str(salt) + "&sign=" + sign
        http_client = fake_http_client_http_connection()
        # Establish a session and return results
        try:
            http_client = http.client.HTTPConnection("api.fanyi.baidu.com")
            http_client.request("GET", target_url)
            # "response" is HTTPResponse object
            response = http_client.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            trans_result = result["trans_result"][0]["dst"]
        except Exception as err:
            logger.critical(repr(err))
            QMessageBox.critical(None, ui["launcher"]["translator"]["title"], ui["translator"]["serverError"],
                                 QMessageBox.StandardButton.Abort)
        finally:
            if http_client:
                http_client.close()
                if trans_result:
                    return trans_result
        return None

    def JSONtoXML(json_file_path: str, xml_file_path: str):
        """
        Convert JSON file to XML file
        Args:
            json_file_path: JSON file path
            xml_file_path: The path to the saved XML file
        Returns:
            0 : Success
            1 : File not found
            2 : The  file failed to be read
        """
        try:
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)
                xml_data = str(eval(dicttoxml.dicttoxml(json_data)))
                with open(xml_file_path, "w", encoding="utf-8") as xml_file:
                    xml_file.write(xml_data)
                    QMessageBox.information(None, "Success", "Converted successfully!")
                    return 0
        except FileNotFoundError:
            logger.error("JSON file not found: {}".format(json_file_path))
            QMessageBox.critical(None, "JSON to XML", ui["fileConverters"]["fileNotFound"],
                                 QMessageBox.StandardButton.Abort)
            return 1
        except Exception as err:
            logger.error(repr(err))
            QMessageBox.critical(None, "JSON to XML", ui["fileConverters"]["otherErrors"],
                                 QMessageBox.StandardButton.Abort)
            return 2

    def XMLtoJSON(xml_file_path: str, json_file_path: str):
        """
        Convert the XML file to a JSON file
        Args:
            xml_file_path: XML file path
            json_file_path: The path to the saved JSON file
        Returns:
            0 : Success
            1 : File not found
            2 : The  file failed to be read
        """
        try:
            with open(xml_file_path, "r", encoding="utf-8") as xml_file:
                xml_data = xml_file.read()
                json_data = json.dumps(xmltodict.parse(
                    xml_data), ensure_ascii=False)
                with open(json_file_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json_data)
                    QMessageBox.information(None, "Success", "Converted successfully!")
                    return 0
        except FileNotFoundError:
            logger.error("JSON file not found: {}".format(json_file_path))
            QMessageBox.critical(None, "XML to JSON", ui["fileConverters"]["fileNotFound"],
                                 QMessageBox.StandardButton.Abort)
            return 1
        except Exception as err:
            logger.error(repr(err))
            QMessageBox.critical(None, "XML to JSON", ui["fileConverters"]["otherErrors"],
                                 QMessageBox.StandardButton.Abort)
            return 2

    def CSVtoJSON(csv_file_path: str, json_file_path: str):
        """
        Convert the CSV file to a JSON file
        Args
            csv_file_path: CSV file path
            json_file_path: The path to the saved JSON file
        Returns:
            0 : Success
            1 : File not found
            2 : The  file failed to be read
        """
        try:
            with open(csv_file_path, "r", encoding="utf-8") as csv_file:
                csv_data = csv_file.read().splitlines()
                json_data = {}
                for csv_line in range(len(csv_data)):
                    json_data[f"line-{str(csv_line + 1)}"] = csv_data[csv_line].split(",")
                with open(json_file_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json.dumps(
                        json_data, ensure_ascii=False, indent=4))
                    QMessageBox.information(None, "Success", "Converted successfully!")
                    return 0
        except FileNotFoundError:
            logger.error("JSON file not found: {}".format(json_file_path))
            QMessageBox.critical(None, "CSV to JSON", ui["fileConverters"]["fileNotFound"],
                                 QMessageBox.StandardButton.Abort)
            return 1
        except Exception as err:
            logger.error(repr(err))
            QMessageBox.critical(None, "CSV to JSON", ui["fileConverters"]["otherErrors"],
                                 QMessageBox.StandardButton.Abort)
            return 2

    def JSONtoCSV(json_file_path: str, csv_file_path: str):
        """
        Convert the JSON file to a CSV file
        Args:
            json_file_path: JSON file path
            csv_file_path: CSV file path
        Returns:
            0 : Success
            1 : File not found
            2 : The  file failed to be read
        """
        try:
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)  # type: dict
                csv_data = []
                for key in json_data.keys():
                    csv_data.append(f"{key},{json_data[key]}\n")
                with open(csv_file_path, "w", encoding="utf-8") as csv_file:
                    csv_file.writelines(csv_data)
                    QMessageBox.information(None, "Success", "Converted successfully!")
                    return 0
        except FileNotFoundError:
            logger.error("JSON file not found: {}".format(json_file_path))
            QMessageBox.critical(None, "JSON to CSV", ui["fileConverters"]["fileNotFound"],
                                 QMessageBox.StandardButton.Abort)
            return 1
        except Exception as err:
            logger.error(repr(err))
            QMessageBox.critical(None, "JSON to CSV", ui["fileConverters"]["otherErrors"],
                                 QMessageBox.StandardButton.Abort)
            return 2

    def getIP(domain=socket.gethostname()):
        """
        Get an IP address
        Args:
            domain: domain name, which defaults to the hostname
        Returns:
            IP address or error message
        """
        try:
            return socket.gethostbyname(domain)
        except socket.error as err:
            return repr(err)

    def resolveDomain(ip):
        """
        Resolve IP addresses
        Args:
            ip: IP address
        Returns:
            Domain names or error messages
        """
        try:
            domain = socket.gethostbyaddr(ip)
            return domain[0]
        except socket.error as err:
            return repr(err)

    class FileDiffTools:  # TODO: 添加功能到主UI
        def __init__(self):
            text1 = QFileDialog.getOpenFileName(None, ui["fileDiff"]["chooseFileOne"], "", "File(*.txt *.*)")[0]
            text2 = QFileDialog.getOpenFileName(None, ui["fileDiff"]["chooseFileTwo"], "", "File(*.txt *.*)")[0]
            result = self.diffTexts(text1, text2,
                                    QFileDialog.getSaveFileName(None, ui["fileDiff"]["saveAs"], "", "File(*.html *.*)")[
                                        0])
            logger.info("Save file successfully!")
            if result == 0:
                QMessageBox.information(None, ui["fileDiff"]["saveAs"], ui["fileDiff"]["success"],
                                        QMessageBox.StandardButton.Abort)
            else:
                QMessageBox.critical(None, ui["error"], ui["fileDiff"]["error"].format(result),
                                     QMessageBox.StandardButton.Abort)

        @staticmethod
        def readFromFile(fpath):
            """
            Read text from a file
            Args:
                fpath: File path
            Returns:
                File content
            """
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read().splitlines()

        @staticmethod
        def diffTexts(text1: str, text2: str, fpath: str):
            """
            Compare two pieces of text and save the result to an HTML file
            Args:
                text1: Text 1
                text2: Text 2
                fpath: The path to the saved HTML file
            Returns:
                0: Success
                1: A problem with the parameters
                2: File read failed
            """
            try:
                html_diff = HtmlDiff()
                diff = html_diff.make_file(text1, text2)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(diff)
                    return 0
            except Exception as err:
                logger.error(repr(err))
                return 2


class ArtTools:
    def charPicture(filename):  # TODO: 添加功能到主UI
        """
        Convert pictures to ascii art
        Args:
            filename: The file name of the image
        """
        color = "MNHQ$OC?7>!:-;."  # characters

        def to_html(func):
            html_head = '''
                    <html>
                        <head>
                            <style type="text/css">
                                body {
                                    font-family: Monospace;
                                    font-size: 5px;
                                }
                            </style>
                        </head>
                    <body> '''
            html_tail = "</body> </html>"

            # HTML definition
            def wrapper(image):
                pic_string = func(image)
                pic_string = "".join(line + " <br />" for line in pic_string.splitlines())
                return html_head + pic_string + html_tail

            return wrapper

        # Draw ascii art
        @to_html
        def make_char_img(image):
            pix = img.load()
            pic_string = ""
            width, height = image.size
            for h in range(height):
                for w in range(width):
                    pic_string += color[int(pix[int(w), int(h)] * 14 / 255)]
                pic_string += "\n"
            return pic_string

        def preprocess(img_name):
            image = Image.open(img_name)
            w, h = image.size
            m = max(image.size)
            delta = m / 200.0
            w, h = int(w / delta), int(h / delta)
            image = image.resize((w, h))
            image = image.convert('L')
            return image

        def save_to_file(filename, pic_str):
            with open(filename, 'w') as outfile:
                logger.debug("File was successfully saved")
                outfile.write(pic_str)

        img = preprocess(filename)
        pic_str = make_char_img(img)
        save_to_file(f"{filename}-char.html", pic_str)
        logger.info(f"Output file:{filename}-char.html")
        QMessageBox.information(None, ui["asciiArt"]["successTitle"], ui["asciiArt"]["successMessage"])

    def bingPicture(filename: str, idx: str = "0", mkt: str = "zh-cn"):  # TODO: 添加功能到主UI
        """
        Get Bing's Daily Graph
        Args:
            filename: The name of the saved file
            idx: Time index
                0: Today
                -1: Tomorrow (pre-prepared)
                1: Yesterday
                2: Day before yesterday
                3~7 analogy
            mkt: Region, using Microsoft region codes, e.g. zh-cn: Chinese mainland, en-us: United States
        Returns:
            Exit code
        """
        try:
            NUMBER = 1
            IDX = idx
            MKT = mkt
            FORMAT = "js"
            USER_AGENT = {
                'Content-Type': 'application/json; charset=utf-8',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/86.0.4240.198 Safari/537.36',
            }
            requestURL = "https://www.bing.com/HPImageArchive.aspx?" + \
                         f"format={FORMAT}&idx={IDX}&n={NUMBER}&mkt={MKT}"
            response = requests.get(requestURL, headers=USER_AGENT)
            if response.status_code == 200:
                try:
                    if NUMBER == 1:
                        data = response.json()
                        data = "https://www.bing.com" + data["images"][0]["url"]
                        with open(filename, 'wb') as f:
                            f.write(requests.get(data).content)
                            return 0
                    else:
                        logger.error("Number of images must be 1")
                        return 1
                except Exception as err:
                    logger.error(f"{repr(err)}")
                    raise err
            else:
                logger.error(f"Network Error: {response.status_code}")
                return 1
        except Exception as err:
            logger.error(f"{repr(err)}")
            return -1


class DevToolsLauncher():

    def __init__(self):
        QMessageBox.critical(None, ui["error"], ui["invocationError"])
        logger.error("Invocation error")

    @staticmethod
    def webConnectTestLauncher():
        url = QInputDialog.getText(None, ui["launchers"]["dev"]["webConnectTest"]["input_url"],
                                   ui["launchers"]["dev"]["webConnectTest"]["input_url"])[0]
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
            result = QMessageBox.question(None, ui["launchers"]["dev"]["translator"]["title"],
                                          ui["launchers"]["dev"]["translator"]["informationRequired"])
            if result == QMessageBox.StandardButton.Yes:
                title = ui["launchers"]["dev"]["translator"]["title"]
                label = ui["launchers"]["dev"]["translator"]["informationInputs"]["message"]
                flags = "\n".join(ui["launchers"]["dev"]["translator"]["informationInputs"]["fields"])
                data = QInputDialog.getMultiLineText(None, title, label, flags)[0].split("\n")
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
            with open("./data/translator.languages.json", "r", encoding="utf-8") as languages_file:
                languages = languages_file.read()
                languages = json.loads(languages)  # type: dict
            global DevTools
            text = QInputDialog.getText(None, ui["launchers"]["dev"]["translator"]["title"],
                                        ui["launchers"]["dev"]["translator"]["inputs"]["text"])[0]
            if text:
                fromLang = "auto"
                toLang = QInputDialog.getItem(None, ui["launchers"]["dev"]["translator"]["title"],
                                              ui["launchers"]["dev"]["translator"]["inputs"]["languageChooseMessage"],
                                              list(languages.keys()), 0, True)
                logger.info(
                    f"User input:[{text}, {fromLang}, {languages[toLang[0]]}]")
                if (text != None) and (fromLang != None) and (toLang[0] != None):
                    result = DevTools.translator(
                        text, id, key, fromLang, languages[toLang[0]])
                    messagebox_text = f"{ui["launchers"]["dev"]["translator"]["completeInformation"]["complete"]}\n \
{ui["launchers"]["dev"]["translator"]["completeInformation"]["original"]}{text}\n \
{ui["launchers"]["dev"]["translator"]["completeInformation"]["result"]} {result}\n \
{ui["launchers"]["dev"]["translator"]["completeInformation"]["language"]} {toLang[0]}"
                    QMessageBox.information(None, ui["launchers"]["dev"]["translator"]["title"], messagebox_text)
                    logger.info(f"Result: {result}")
                else:
                    QMessageBox.critical(None, ui["launchers"]["dev"]["translator"]["title"],
                                         ui["launchers"]["dev"]["translator"]["errorInformationMessage"])
                    logger.error("Missing arguments")

    @staticmethod
    def JSONtoXMLLauncher():
        json = QFileDialog.getOpenFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["openTitle"],
                                           "", "JSON File(*.json)")[0]
        xml = QFileDialog.getSaveFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["saveTitle"],
                                          "", "XML File(*.xml)")[0]
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
        xml = QFileDialog.getOpenFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["openTitle"],
                                          "", "XML Files(*.xml)")[0]
        json = QFileDialog.getSaveFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["saveTitle"],
                                           "", "JSON File(*.json)")[0]
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
        ip = QInputDialog.getText(None, ui["launchers"]["dev"]["socketTools"]["getIP"]["title"],
                                  ui["launchers"]["dev"]["socketTools"]["getIP"]["inputMessage"])[0]
        if (ip != None):
            if (ip != "@default"):
                logger.info(f"Input IP:{ip}")
                result = DevTools.getIP(ip)
                QMessageBox.information(None, ui["launchers"]["dev"]["socketTools"]["getIP"]["title"],
                                        f"{ui["launchers"]["dev"]["socketTools"]["getIP"]["ip"]} {result}")
                logger.info(f"Result: {result}")
            else:
                logger.info(f"Input IP:{ip}")
                result = DevTools.getIP()
                QMessageBox.information(None, ui["launchers"]["dev"]["socketTools"]["getIP"]["title"],
                                        f"{ui["launchers"]["dev"]["socketTools"]["getIP"]["ip"]} {result}")
                logger.info(f"Result: {result}")

    @staticmethod
    def resolveDomainLauncher():
        domain = QInputDialog.getText(None, ui["launchers"]["dev"]["socketTools"]["resolveDomain"]["Domain"],
                                      ui["launchers"]["dev"]["socketTools"]["resolveDomain"]["input"])[0]
        if (domain != None):
            global DevTools
            logger.info(f"Input Domain: {domain}")
            result = DevTools.resolveDomain(domain)
            QMessageBox.information(None, ui["launchers"]["dev"]["socketTools"]["resolveDomain"]["title"],
                                    f"{ui["launchers"]["dev"]["socketTools"]["resolveDomain"]["Domain"]} {result}")
            logger.info(f"Result: {result}")

    @staticmethod
    def JSONtoCSVLauncher():
        json = QFileDialog.getOpenFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["openTitle"],
                                           "", "JSON File(*.json)")[0]
        csv = QFileDialog.getSaveFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["saveTitle"],
                                          "", "CSV File(*.csv)")[0]
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
        csv = QFileDialog.getOpenFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["openTitle"],
                                          "", "CSV File(*.csv)")[0]
        json = QFileDialog.getSaveFileName(None, ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["saveTitle"],
                                           "", "JSON File(*.json)")[0]
        
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
        path = QFileDialog.getOpenFileName(None, ui["launchers"]["art"]["asciiArt"]["open"],
                                           "", "Image(*.png *.gif)")[0]
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
        filename = QFileDialog.getSaveFileName(None, ui["launchers"]["art"]["bingPicture"]["saveAs"],
                                               "", "Image(*.jpg *.*)")[0]
        if (filename != None):
            logger.info(f"Input path: {filename}")
            if (os.path.splitext(filename)[-1] == ".jpg"):
                params = QInputDialog.getMultiLineText(None, ui["launchers"]["art"]["bingPicture"]["title"],
                                                       ui["launchers"]["art"]["bingPicture"]["inputs"]["msg"],
                                                       "\n".join(
                                                           ui["launchers"]["art"]["bingPicture"]["inputs"]["fields"]
                                                       ))[0].split("\n")
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
            subprocess.Popen("python ./src/webspeedtest/main.py")
        QMessageBox.warning(None, ui["warn"], ui["launchers"]["external"]["webSpeedTestWarning"])
        thread = threading.Thread(target=run)
        thread.start()

    @staticmethod
    def clockLauncher():
        subprocess.Popen("python ./src/clock/main.py")

    @staticmethod
    def calculatorLauncher():
        subprocess.Popen("python ./src/calculator/main.py")

    @staticmethod
    def hashCheckerLauncher():
        QMessageBox.information(None, "Python Utilities", ui["launchers"]["external"]["hashCheckerWarning"])

    @staticmethod
    def passwordCreatorLauncher():
        subprocess.Popen("python ./src/passwordCreator/main.py")

    @staticmethod
    def licenceCreatorLauncher():
        subprocess.Popen("python ./src/licenceCreator/main.py")

    @staticmethod
    def qrcodeGeneratorLauncher():
        subprocess.Popen("python ./src/qrcode/encoder.py")

    @staticmethod
    def qrcodeParserLauncher():
        subprocess.Popen("python ./src/qrcode/decoder.py")

    @staticmethod
    def weatherLauncher():
        subprocess.Popen("python ./src/weather/main.py")

    @staticmethod
    def speech2textLauncher():
        subprocess.Popen("python ./src/speech2text/main.py")

    @staticmethod
    def pictureFormatConverterLauncher():
        subprocess.Popen("python ./src/photo_format_converter/main.py")

    @staticmethod
    def sendMailFromJSONLauncher():
        subprocess.Popen("python ./src/send_mail_from_json/main.py")

    @staticmethod
    def AMKLauncher():
        subprocess.Popen("python ./src/auto_mouse_and_keyboard/main.py")

    @staticmethod
    def countDownLauncher():
        subprocess.Popen("python ./src/count_down/main.py")

    @staticmethod
    def pinyinLauncher():
        subprocess.Popen("python ./src/Chinese_Pinyin_Dictionary/main.py")

    @staticmethod
    def captchaLauncher():
        subprocess.Popen("python ./src/Captcha_Generator/main.py")

    @staticmethod
    def toDoLauncher():
        subprocess.Popen("python ./src/EasyTodo/main.py")

    @staticmethod
    def OCRLauncher():
        subprocess.Popen("python ./src/ocr/main.py")

    @staticmethod
    def chinesePinyinDictionaryLauncher():
        subprocess.Popen("python ./src/Chinese_Pinyin_Dictionary/main.py")
