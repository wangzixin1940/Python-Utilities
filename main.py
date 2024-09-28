from difflib import HtmlDiff
import tkinter.filedialog as fdg
import socket
import dicttoxml
import xmltodict
import threading
import subprocess
import random
import urllib
import hashlib
import http.client
from PIL import Image
import requests
import platform
import datetime
import logging
import easygui
import ttkbootstrap as ttk
from tkinter import messagebox as msgbox
import os
import json

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

sysinfo = {
    "system": platform.system(),
    "version": platform.version(),
    "python": {
        "version": platform.pythonVersion().split("."),
        "implementation": platform.python_implementation(),
    }
}
for i in range(len(sysinfo["python"]["version"])):
    if not ("b" in str(sysinfo["python"]["version"][i])):
        sysinfo["python"]["version"][i] = int(sysinfo["python"]["version"][i])
    else:
        sysinfo["python"]["version"][i] = sysinfo["python"]["version"][i].split("b")[
            0]


class DevTools():
    def __init__(self):
        msgbox.showerror(title=ui["error"], message=ui["invocationError"])
        logger.error("Invocation error")

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
        # If the HTTP status code is known, the result is returned. Otherwise, the user is prompted to return an unknown status code

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
            msgbox.showerror(
                message=ui["translator"]["serverError"],
                title=ui["launcher"]["translator"]["title"])
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
            msgbox.showerror(message=ui["fileConverters"]["fileNotFound"], title="JSON to XML")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message=ui["fileConverters"]["otherErrors"], title="JSON to XML")
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
            msgbox.showerror(message=ui["fileConverters"]["fileNotFound"], title="JSON to XML")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message=ui["fileConverters"]["otherErrors"], title="JSON to XML")
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
            msgbox.showerror(message=ui["fileConverters"]["fileNotFound"], title="JSON to XML")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message=ui["fileConverters"]["otherErrors"], title="JSON to XML")
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
            msgbox.showerror(message=ui["fileConverters"]["fileNotFound"], title="JSON to XML")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message=ui["fileConverters"]["otherErrors"], title="JSON to XML")
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

    class FileDiffTools():
        def __init__(self):
            text1 = self.readFromFile(
                fdg.askopenfilename(title=ui["fileDiff"]["chooseFileOne"],
                                    filetypes=(file_types["txt"], file_types["all"])))
            text2 = self.readFromFile(
                fdg.askopenfilename(title=ui["fileDiff"]["chooseFileOne"],
                                    filetypes=((file_types["txt"]), file_types["all"])))
            result = self.diffTexts(text1, text2, fdg.asksaveasfilename(title=ui["fileDiff"]["saveAs"], filetypes=(
                file_types["html"], file_types["all"])))
            logger.info("Save file successfully!")
            if result == 0:
                msgbox.showinfo(title=ui["fileDiff"]["success"], message="保存文件成功！")
            else:
                msgbox.showerror(
                    title=ui["error"], message=ui["fileDiff"]["error"].format(result))

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


class DrawingTools():
    def __init__(self):
        msgbox.showerror(title=ui["error"], message=ui["invocationError"])
        logger.error("Invocation error")

    def charPicture(filename):
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
        msgbox.showinfo(title=ui["asciiArt"]["successTitle"], message=ui["asciiArt"]["successMessage"])

    def bingPicture(fname: str, idx: str = "0", mkt: str = "zh-cn"):
        """
        Get Bing's Daily Graph
        Args:
            fname: The name of the saved file
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
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            }
            requestURL = "https://cn.bing.com/HPImageArchive.aspx?" + \
                         f"format={FORMAT}&idx={IDX}&n={NUMBER}&mkt={MKT}"
            response = requests.get(requestURL, headers=USER_AGENT)
            if (response.status_code == 200):
                try:
                    if NUMBER == 1:
                        data = response.json()
                        data = "https://cn.bing.com" + data["images"][0]["url"]
                        with open(fname, 'wb') as f:
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


class Launcher():
    def __init__(self):
        msgbox.showerror(title=ui[ui["error"]], message=ui["invocationError"])
        logger.error("Invocation error")

    class DevToolsLauncher():
        def __init__(self):
            msgbox.showerror(title=ui["error"], message=ui["invocationError"])
            logger.error("Invocation error")

        @staticmethod
        def webConnectTestLauncher():
            try:
                with open("logs/records.log", "r") as r:
                    try:
                        record = r.readlines()[len(r.readlines()) - 1]
                    except IndexError:
                        record = ""
            except FileNotFoundError:
                record = ""
            url = easygui.enterbox(
                msg=ui["launchers"]["dev"]["input_url"], title="Python Utilities", default=record)
            logger.info(f"User input: {url}")
            if (url != None):
                record = url
                if not (settings["no-log-file"]):
                    with open("logs/records.log", "a") as record_log:
                        record_log.write(f"\n{record}")
            if (url != None):
                global DevTools
                result = DevTools.webConnectTest(url)
                error_list = ui["launchers"]["dev"]["error_list"]
                msgbox.showinfo(title="Python Utilities", message=error_list[str(result)])
                if not (1 == result or 2 == result):
                    logger.info(f"Web address connect info: {url} => {result}")
                    msgbox.showinfo(title="Python Utilties", message=result)
                else:
                    msgbox.showinfo(title="Python Utilties",
                                    message=error_list[result - 1])

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
                result = msgbox.askokcancel(
                    message=ui["launchers"]["dev"]["translator"]["informationRequired"],
                    title=ui["launchers"]["dev"]["translator"]["title"], icon="warning")
                if result:
                    datas = easygui.multpasswordbox(
                        ui["launchers"]["dev"]["translator"]["informationInputs"]["message"],
                        title=ui["launchers"]["dev"]["translator"]["title"],
                        fields=ui["launchers"]["dev"]["translator"]["informationInputs"]["firlds"])
                    if datas != None:
                        id = datas[0]
                        key = datas[1]
                        entered = True
                        with open("data/translator.appid.json", "w") as appid:
                            appid.write(json.dumps({"id": id, "key": key}))
                    else:
                        entered = False
                else:
                    entered = False
            if (entered):
                with open("./data/translator.languages.json", "r") as languages:
                    languages = languages.read()
                    languages = json.loads(languages)
                global DevTools
                text = easygui.enterbox(ui["launchers"]["dev"]["translator"]["inputs"]["text"],
                                        title=ui["launchers"]["dev"]["translator"]["title"])
                if text:
                    fromLang = "auto"
                    toLang = easygui.choicebox(
                        ui["launchers"]["dev"]["translator"]["inputs"]["languageChooseMessage"],
                        choices=list(languages.keys()),
                        title=ui["launchers"]["dev"]["translator"]["title"])
                    logger.info(
                        f"User input:[{text}, {fromLang}, {languages[toLang]}]")
                    if (text != None) and (fromLang != None) and (toLang != None):
                        result = DevTools.translator(
                            text, id, key, fromLang, languages[toLang])
                        msgbox.showinfo(
                            message=f"{ui["launchers"]["dev"]["translator"]["completeInformation"]["complete"]}\n \
                            {ui["launchers"]["dev"]["translator"]["completeInformation"]["original"]}{text}\n \
                            {ui["launchers"]["dev"]["translator"]["completeInformation"]["result"]} {result}\n \
                            {ui["launchers"]["dev"]["translator"]["completeInformation"]["language"]} {toLang}",
                            title=ui["launchers"]["dev"]["translator"]["title"])
                        logger.info(f"Result: {result}")
                    else:
                        msgbox.showerror(message=ui["launchers"]["dev"]["translator"]["errorInformationMessage"],
                                         title=ui["launchers"]["dev"]["translator"]["title"])
                        logger.error("Missing arguments")

        @staticmethod
        def JSONtoXMLLauncher():
            json = easygui.fileopenbox(title=ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["open_file"],
                                       filetypes=[file_types["json"]], default="*.json")
            xml = easygui.filesavebox(title=ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["save_file"],
                                      filetypes=[file_types["xml"]], default="*.xml")
            if (json != None):
                if (os.path.splitext(json)[-1] == ".json"):
                    global DevTools
                    logger.info(f"Input JSON:{json}")
                    DevTools.JSONtoXML(json, xml)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(title=ui["error"],
                                     message=ui["launchers"]["dev"]["fileConverters"]["extensionError"])
                    logger.error("File extension is incorrect")

        @staticmethod
        def XMLtoJSONLauncher():
            xml = easygui.fileopenbox(title=ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["open_file"],
                                      filetypes=[file_types["xml"]], default="*.xml")
            json = easygui.filesavebox(title=ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["save_file"],
                                       filetypes=[file_types["json"]], default="*.json")
            if (xml != None):
                if (os.path.splitext(xml)[-1] == ".xml"):
                    global DevTools
                    logger.info(f"Input XML:{xml}")
                    DevTools.XMLtoJSON(xml, json)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(title=ui["error"],
                                     message=ui["launchers"]["dev"]["fileConverters"]["extensionError"])
                    logger.error("File extension is incorrect")

        @staticmethod
        def getIPLauncher():
            global DevTools
            ip = easygui.enterbox(
                ui["launchers"]["dev"]["socketTools"]["getIP"]["inputMessage"],
                title=ui["launchers"]["dev"]["socketTools"]["getIP"]["title"])
            if (ip != None):
                if (ip != "@default"):
                    global DevTools
                    logger.info(f"Input IP:{ip}")
                    result = DevTools.getIP(ip)
                    msgbox.showinfo(message=f"{ui["launchers"]["dev"]["socketTools"]["getIP"]["ip"]} {result}",
                                    title=ui["launchers"]["dev"]["socketTools"]["getIP"]["title"])
                    logger.info(f"Result: {result}")
                else:
                    logger.info(f"Input IP:{ip}")
                    result = DevTools.getIP()
                    msgbox.showinfo(message=f"{ui["launchers"]["dev"]["socketTools"]["getIP"]["ip"]} {result}",
                                    title=ui["launchers"]["dev"]["socketTools"]["getIP"]["title"])
                    logger.info(f"Result: {result}")

        @staticmethod
        def resolveDomainLauncher():
            domain = easygui.enterbox(ui["launchers"]["dev"]["socketTools"]["resolveDoamin"]["input"],
                                      title=ui["launchers"]["dev"]["socketTools"]["resolveDoamin"]["doamin"])
            if (domain != None):
                global DevTools
                logger.info(f"Input Domain: {domain}")
                result = DevTools.resolveDomain(domain)
                msgbox.showinfo(message=f"{ui["launchers"]["dev"]["socketTools"]["resolveDoamin"]["doamin"]} {result}",
                                title=ui["launchers"]["dev"]["socketTools"]["resolveDoamin"]["title"])
                logger.info(f"Result: {result}")

        @staticmethod
        def JSONtoCSVLauncher():
            json = easygui.fileopenbox(title=ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["open_file"],
                                       filetypes=[file_types["json"]], default="*.json")
            csv = easygui.filesavebox(title=ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["save_file"],
                                      filetypes=[file_types["csv"]], default="*.csv")
            if (json != None):
                if (os.path.splitext(json)[-1] == ".json"):
                    global DevTools
                    logger.info(f"Input JSON:{json}")
                    DevTools.JSONtoCSV(json, csv)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(title=ui["error"],
                                     message=ui["launchers"]["dev"]["fileConverters"]["extensionError"])
                    logger.error("File extension is incorrect")

        @staticmethod
        def CSVtoJSONLauncher():
            csv = easygui.fileopenbox(title=ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["open_file"],
                                      filetypes=[file_types["csv"]], default="*.csv")
            json = easygui.filesavebox(title=ui["launchers"]["dev"]["fileConverters"]["chooseFile"]["save_file"],
                                       filetypes=[file_types["json"]], default="*.json")
            if (csv != None):
                if (os.path.splitext(csv)[-1] == ".csv"):
                    global DevTools
                    logger.info(f"Input CSV:{csv}")
                    DevTools.CSVtoJSON(csv, json)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(title=ui["error"],
                                     message=ui["launchers"]["dev"]["fileConverters"]["extensionError"])
                    logger.error("File extension is incorrect")

    class DrawingToolsLauncher():
        def __init__(self):
            msgbox.showerror(title=ui["error"], message=ui["invocationError"])
            logger.error("Invocation error")

        @staticmethod
        def charPictureLauncher():
            path = easygui.fileopenbox(title=ui["launchers"]["art"]["asciiArt"]["open"],
                                       filetypes=[file_types["images"]["png"], file_types["images"]["bmp"],
                                                  file_types["images"]["gif"]], default="*.png")
            if (path != None):
                if (os.path.splitext(path)[-1] == ".png") or (os.path.splitext(path)[-1] == ".jpg") or (
                        os.path.splitext(path)[-1] == ".bmp") or (os.path.splitext(path)[-1] == ".gif") or (
                        os.path.splitext(path)[-1] == ".jpeg"):
                    global DrawingTools
                    logger.info(f"Input picture:{path}")
                    DrawingTools.charPicture(path)
                else:
                    msgbox.showerror(title=ui["error"], message=ui["launchers"]["art"]["asciiArt"]["extensionErroror"])
                    logger.error("File extension is incorrect")

        @staticmethod
        def bingPictureLauncher():
            fname = fdg.asksaveasfilename(title=ui["launchers"]["art"]["bingPicture"]["saveAs"],
                                          filetypes=[file_types["images"]["jpg"]],
                                          defaultextension="*.jpg")
            if (fname != None):
                logger.info(f"Input path: {fname}")
                if (os.path.splitext(fname)[-1] == ".jpg"):
                    params = easygui.multenterbox(
                        title=ui["launchers"]["art"]["bingPicture"]["title"],
                        msg=ui["launchers"]["art"]["bingPicture"]["inputs"]["msg"],
                        fields=ui["launchers"]["art"]["bingPicture"]["inputs"]["fields"])
                    if (params != None != ["", ""]):
                        if (params[0].isdigit()) or (params[0] == "-1"):
                            params.insert(0, fname)
                            logger.info(f"Input params:{params}")
                            global DrawingTools
                            DrawingTools.bingPicture(
                                params[0], params[1], params[2])
                            logger.info("Done.")
                            msgbox.showinfo(title=ui["info"],
                                            message=ui["launchers"]["art"]["bingPicture"]["success"])
                        else:
                            msgbox.showerror(title=ui["error"],
                                             message=ui["launchers"]["art"]["bingPicture"]["indexError"])
                            return
                else:
                    logger.error("File extension is incorrect")
                    msgbox.showerror(title=ui["error"],
                                     message=ui["launchers"]["art"]["bingPicture"]["extensionError"])
                    return

    class ExternalLauncher():
        def __init__(self):
            msgbox.showerror(title=ui["error"], message=ui["invocationError"])
            logger.error("Invocation error")

        @staticmethod
        def webSpeedTsetLauncher():
            def run():
                subprocess.Popen("python /src/webspeedtest/main.py")

            msgbox.showwarning(title=ui["warn"],
                               message=ui["launchers"]["external"]["webSpeedTestWarning"])
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
            msgbox.showinfo(title="Python Utilities",
                            message=ui["launchers"]["external"]["hashCheckerWarning"])

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
            subprocess.Popen("python src/phot_format_converter/main.py")

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
        def doWorkLauncher():
            subprocess.Popen("python src/EasyTodo/main.py")


class System():
    @staticmethod
    def about():
        msgbox.showinfo(title="Python Utilities", message=ui["system"]["about"])

    @staticmethod
    def languageSettings():
        filepath = fdg.askopenfilename(title="Select Language File", filetypes=[("JSON Files", "*.json")],
                                       defaultextension="*.json")
        if (filepath):
            if (msgbox.askokcancel(title="Windows Utilitles",
                                   message=f"You choosed the file \"{filepath}\".\n" +
                                           "Are you sure you want to use this file?" +
                                           "Make sure this profile is complete and don't delete it in the future" +
                                           "(unless you change it).")):
                settings["language"] = filepath
                with open("data/settings.json", "w", encoding="utf-8") as file:
                    json.dump(settings, file, indent=4, ensure_ascii=False)
                    if (easygui.buttonbox(title="Windows Utilitles",
                                          msg="You'll have to restart the program to apply the changes.",
                                          choices=["Restart Now", "Restart later"], default_choice="Restart Now",
                                          cancel_choice="Restart later") == "Restart Now"):
                        root.destroy()
                        os.system("python main.py")

    @staticmethod
    def quitApp():
        root.destroy()

    def switchTheme(theme_name):
        if (theme_name == "pride"):
            root.iconbitmap("./images/pride.ico")
            style.theme_use("cosmo")
            style.configure("TButton", font=(
                "Helvetica", 18, "normal"), width=20, height=3)
            style.configure("TMenubutton", font=(
                "Helvetica", 18, "normal"), width=19, height=3)
        else:
            root.iconbitmap("./images/icon.ico")
            style.theme_use(theme_name)
            style.configure("TButton", font=(
                "Helvetica", 18, "normal"), width=20, height=3)
            style.configure("TMenubutton", font=(
                "Helvetica", 18, "normal"), width=19, height=3)
        theme["theme"] = theme_name
        with open("./data/theme.json", "w") as f:
            json.dump(theme, f)

    @staticmethod
    def importSettings():
        path = easygui.fileopenbox(title=ui["system"]["importSettings"]["open"], filetypes=[
            ["*.json", "JSON files"]], default="*.json")
        global settings
        if (path != None):
            if (msgbox.askokcancel(title="Python Utilities",
                                   message=ui["system"]["importSettings"]["warning"],
                                   icon="warning")):
                with open(path, "r+", encoding="utf-8") as new_settings:
                    new_settings = new_settings.read()
                    new_settings = json.loads(new_settings)
                    logger.info(f"Settings: {new_settings}")
                    with open("data/settings.json", "w+", encoding="utf-8") as settings:
                        settings.write(json.dumps(
                            new_settings, ensure_ascii=False, indent=4))
                        msgbox.showinfo(
                            title="Python Utilities", message=ui["system"]["importSettings"]["complete"])
                        logger.info("Settings imported")


def main():
    global root
    global style
    global theme
    root = ttk.Window()
    with open("./data/theme.json", "r", encoding="utf-8") as theme:
        theme = theme.read()
        theme = json.loads(theme)
    logger.info("Starting APP")
    root.title("Python Utilities")
    root.geometry("{}x{}".format(
        settings["geometry"][0], settings["geometry"][1]))
    root.resizable(settings["resizable"][0], settings["resizable"][1])
    if settings["icon-file-path"] == "@default":
        if theme["theme"] == "pride":
            root.iconbitmap("./images/pride.ico")
            style = ttk.Style("cosmo")
        else:
            root.iconbitmap("./images/icon.ico")
            style = ttk.Style(theme["theme"])
    else:
        if os.path.exists(settings["icon-file-path"]):
            root.iconbitmap(settings["icon-file-path"])
            style = ttk.Style("cosmo")
        else:
            root.iconbitmap("./images/icon.ico")
            style = ttk.Style("cosmo")
            logger.warning(
                "Icon file not found. Program will use default icon and cosmo theme.")
    style.configure("TButton", font=(
        "Helvetica", 18, "normal"), width=20, height=3)
    style.configure("TMenubutton", font=(
        "Helvetica", 18, "normal"), width=19, height=3)
    # Window
    main_ui_src = ui["ui"]
    menu_src = ui["ui"]["menus"]
    # ===================================== #
    title = ttk.Label(root, text="Python Utilities",
                      font=("Helvetica", 22, "normal"))
    title.pack()  # The title of this program
    # ===================================== #
    utilitiesLabel = ttk.Label(
        root, text=main_ui_src["utilities"]["title"], font=("Helvetica", 18, "normal"))
    utilitiesLabel.pack()  # Utilities label
    translateButton = ttk.Button(text=main_ui_src["utilities"]["translator"],
                                 command=Launcher.DevToolsLauncher.translatorLauncher,
                                 bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    translateButton.pack()  # Translator button
    weatherButton = ttk.Button(root, text=main_ui_src["utilities"]["weatherReport"],
                               command=Launcher.ExternalLauncher.weatherLauncher,
                               bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    weatherButton.pack()  # Weather forecast button
    speech2textButton = ttk.Button(root, text=main_ui_src["utilities"]["speech2text"],
                                   command=Launcher.ExternalLauncher.speech2textLauncher,
                                   bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speech2textButton.pack()  # Speech-to-text button
    doWorkButton = ttk.Button(root, text=main_ui_src["utilities"]["to-do"],
                              command=Launcher.ExternalLauncher.doWorkLauncher,
                              bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    doWorkButton.pack()  # Easy To Do button
    # ===================================== #
    DevToolsLabel = ttk.Label(root, text=main_ui_src["dev"]["title"],
                              font=("Helvetica", 18, "normal"))
    DevToolsLabel.pack()  # Developer Tools label
    connectButton = ttk.Button(text=main_ui_src["dev"]["connectInformation"],
                               command=Launcher.DevToolsLauncher.webConnectTestLauncher,
                               bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    connectButton.pack()  # Detect network connections
    # speedTestButton = ttk.Button(root, text=main_ui_src["dev"]["speedtest"], command=Launcher.ExternalLauncher.webSpeedTsetLauncher,
    #                              bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    # speedTestButton.pack()  # Speed test button (deprecated)
    # ===================================== #
    externalsLabel = ttk.Label(
        root, text=main_ui_src["others"]["title"], font=("Helvetica", 18, "normal"))
    externalsLabel.pack()  # Other Tools tabs
    passwordCreatorButton = ttk.Button(root, text=main_ui_src["others"]["passwordCreator"],
                                       command=Launcher.ExternalLauncher.passwordCreatorLauncher,
                                       bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    passwordCreatorButton.pack()  # Password generator button
    # ===================================== #
    if not (settings["no-menu"]):
        menu = ttk.Menu(root)
        fileMenu = ttk.Menu(menu)
        otherMenu = ttk.Menu(menu)
        settingsMenu = ttk.Menu(menu)
        menu.add_cascade(label=menu_src["file"]["title"], menu=fileMenu)
        menu.add_cascade(label=menu_src["other"]["title"], menu=otherMenu)
        if not (settings["no-settings-menu"]):
            menu.add_cascade(label=menu_src["settings"]["title"], menu=settingsMenu)
        menu.add_command(label=menu_src["about"], command=System.about)
        fileMenu.add_command(label=menu_src["file"]["importSettings"], command=System.importSettings)
        fileMenu.add_command(label=menu_src["file"]["exit"], command=System.quitApp)
        otherMenu.add_command(
            label=menu_src["other"]["calculator"], command=Launcher.ExternalLauncher.calculatorLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["hashChecker"], command=Launcher.ExternalLauncher.hashCheckerLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["licenceCreator"], command=Launcher.ExternalLauncher.licenceCreatorLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["smfj"], command=Launcher.ExternalLauncher.sendMailFromJSONLauncher)
        ipToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label=menu_src["other"]["ipTools"]["title"], menu=ipToolsMenu)
        ipToolsMenu.add_command(
            label=menu_src["other"]["ipTools"]["getIP"], command=Launcher.DevToolsLauncher.getIPLauncher)
        ipToolsMenu.add_command(
            label=menu_src["other"]["ipTools"]["resolveDoamin"],
            command=Launcher.DevToolsLauncher.resolveDomainLauncher)
        fileToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label=menu_src["other"]["fileTools"]["title"], menu=fileToolsMenu)
        fileToolsMenu.add_command(
            label=menu_src["other"]["fileTools"]["jsonToXml"], command=Launcher.DevToolsLauncher.JSONtoXMLLauncher)
        fileToolsMenu.add_command(
            label=menu_src["other"]["fileTools"]["xmlToJson"], command=Launcher.DevToolsLauncher.XMLtoJSONLauncher)
        fileToolsMenu.add_command(
            label=menu_src["other"]["fileTools"]["jsonToCsv"], command=Launcher.DevToolsLauncher.JSONtoCSVLauncher)
        fileToolsMenu.add_command(
            label=menu_src["other"]["fileTools"]["csvToJson"], command=Launcher.DevToolsLauncher.CSVtoJSONLauncher)
        fileToolsMenu.add_command(label=menu_src["other"]["fileTools"]["diff"], command=DevTools.FileDiffTools)
        qrcodeToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label=menu_src["other"]["qrcodeTools"]["title"], menu=qrcodeToolsMenu)
        qrcodeToolsMenu.add_command(
            label=menu_src["other"]["qrcodeTools"]["generate"],
            command=Launcher.ExternalLauncher.qrcodeGeneratorLauncher)
        qrcodeToolsMenu.add_command(
            label=menu_src["other"]["qrcodeTools"]["parse"], command=Launcher.ExternalLauncher.qrcodeParserLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(
            label=menu_src["other"]["asciiArt"], command=Launcher.DrawingToolsLauncher.charPictureLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["bingPicture"], command=Launcher.DrawingToolsLauncher.bingPictureLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["pictureConvertor"],
            command=Launcher.ExternalLauncher.pictureFormatConverterLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["amk"], command=Launcher.ExternalLauncher.AMKLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["captcha"], command=Launcher.ExternalLauncher.captchaLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(
            label=menu_src["other"]["clock"], command=Launcher.ExternalLauncher.clockLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["countDown"], command=Launcher.ExternalLauncher.countDownLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["pinyinDictionary"], command=Launcher.ExternalLauncher.pinyinLauncher)
        if not (settings["no-settings-menu"]):
            themesMenu = ttk.Menu(settingsMenu)
            settingsMenu.add_cascade(label=menu_src["settings"]["themes"], menu=themesMenu)
            for i in style.theme_names():
                themesMenu.add_radiobutton(
                    label=i, command=lambda name=i: System.switchTheme(name)
                )
            themesMenu.add_separator()
            themesMenu.add_command(
                label="pride", command=lambda: System.switchTheme("pride"))
            settingsMenu.add_command(
                label="Choose language profile", command=System.languageSettings)
        root.config(menu=menu)
    # Toolbar
    # ===================================== #
    root.mainloop()


if __name__ == '__main__':
    logger.info("Platform: {system} {version}".format(
        system=sysinfo["system"], version=sysinfo["version"]))
    logger.info("Python: {version} {implementation}".format(version=sysinfo["python"]["version"],
                                                            implementation=sysinfo["python"]["implementation"]))
    # Outputs system information
    if sysinfo["python"]["version"][0] >= 3:
        if sysinfo["python"]["version"][1] >= 8:
            main()
            exit(0)
        else:
            logger.warning("Python Version too old: {}".format(
                sysinfo["python"]["version"]))
    else:
        logger.warning("Python Version too old: {}".format(
            sysinfo["python"]["version"]))
    main()
    exit(1)
