import os

with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the standard output


os.chdir(os.path.dirname(__file__))
# Change the working directory to the directory of the script

with open("../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)  # type: dict[str: dict]


import requests
import json
import logging
import datetime
import random
import hashlib
import urllib
import http
import dicttoxml, xmltodict, socket
from difflib import HtmlDiff
from PySide6.QtWidgets import QMessageBox, QFileDialog, QApplication


app = QApplication([])

logging.basicConfig(
        filename=f"../logs/{datetime.date.today()}.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("DEVTOOLS")


def webConnectTest(url: str):
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
        QMessageBox.critical(None, ui["launcher"]["translator"]["title"], ui["translator"]["serverError"], QMessageBox.StandardButton.Abort)
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
            xml_data = str(dicttoxml.dicttoxml(json_data))
            with open(xml_file_path, "w", encoding="utf-8") as xml_file:
                xml_file.write(xml_data)
                return 0
    except FileNotFoundError:
        logger.error("JSON file not found: {}".format(json_file_path))
        QMessageBox.critical(None, "JSON to XML", ui["fileConverters"]["fileNotFound"], QMessageBox.StandardButton.Abort)
        return 1
    except Exception as err:
        logger.error(repr(err))
        QMessageBox.critical(None, "JSON to XML", ui["fileConverters"]["otherErrors"], QMessageBox.StandardButton.Abort)
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
                return 0
    except FileNotFoundError:
        logger.error("JSON file not found: {}".format(json_file_path))
        QMessageBox.critical(None, "XML to JSON", ui["fileConverters"]["fileNotFound"], QMessageBox.StandardButton.Abort)
        return 1
    except Exception as err:
        logger.error(repr(err))
        QMessageBox.critical(None, "XML to JSON", ui["fileConverters"]["otherErrors"], QMessageBox.StandardButton.Abort)
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
                return 0
    except FileNotFoundError:
        logger.error("JSON file not found: {}".format(json_file_path))
        QMessageBox.critical(None, "CSV to JSON", ui["fileConverters"]["fileNotFound"], QMessageBox.StandardButton.Abort)
        return 1
    except Exception as err:
        logger.error(repr(err))
        QMessageBox.critical(None, "CSV to JSON", ui["fileConverters"]["otherErrors"], QMessageBox.StandardButton.Abort)
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
                return 0
    except FileNotFoundError:
        logger.error("JSON file not found: {}".format(json_file_path))
        QMessageBox.critical(None, "JSON to CSV", ui["fileConverters"]["fileNotFound"], QMessageBox.StandardButton.Abort)
        return 1
    except Exception as err:
        logger.error(repr(err))
        QMessageBox.critical(None, "JSON to CSV", ui["fileConverters"]["otherErrors"], QMessageBox.StandardButton.Abort)
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

class FileDiffTools:
    def __init__(self):
        text1 = QFileDialog.getOpenFileName(None, ui["fileDiff"]["chooseFileOne"], "", "File(*.txt *.*)")[0]
        text2 = QFileDialog.getOpenFileName(None, ui["fileDiff"]["chooseFileTwo"], "", "File(*.txt *.*)")[0]
        result = self.diffTexts(text1, text2, QFileDialog.getSaveFileName(None, ui["fileDiff"]["saveAs"], "", "File(*.html *.*)"))
        logger.info("Save file successfully!")
        if result == 0:
            QMessageBox.information(None, ui["fileDiff"]["saveAs"], ui["fileDiff"]["success"], QMessageBox.StandardButton.Abort)
        else:
            QMessageBox.critical(None, ui["error"], ui["fileDiff"]["error"].format(result), QMessageBox.StandardButton.Abort)

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
