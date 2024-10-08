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
    # Read settings.json

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change encoding to settings["encoding"]

os.chdir(os.path.dirname(__file__))
# Change current directory to the script's directory

# Reserved modules

# Modules required for the tool

if not (settings["no-log-file"]):
    logging.basicConfig(
        filename=f"./logs/{datetime.date.today()}.log",
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
# Configure log information

sysinfo = {
    "system": platform.system(),
    "version": platform.version(),
    "python": {
        "version": platform.python_version().split("."),
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
        msgbox.showerror(
            title="Error", message="Call error! Please call the children of this class.")
        logger.error("Invocation error")

    def webConnectTest(url: str):
        """
        Test if the website is accessible
        Args:
            url: website URL
        Returns:
            Exit code
        """
        try:
            result = str(requests.get(url).status_code)
        except requests.exceptions.MissingSchema:
            logger.critical("Missing schema error")
            return 1
        # Return http status code
        with open("./data/connect.test.codes.json", "r") as statusCodes:
            statusCodes = statusCodes.read()
            statusCodes = json.loads(statusCodes)
        # A list of common http status codes
        try:
            return str(result) + " : " + statusCodes[result]
        except KeyError:
            logger.error(f"Status code: {result} not found")
            return 2
        # If the http status code is known, the result is returned. Otherwise, the user is prompted to return an unknown status code

    def translator(text: str, appid: str, secret_key: str, original_language: str, target_language: str):
        """
        Translate text using Baidu Translate API
        Args:
            text: Texts that need to be translated
            appid: Baidu Translate API's appid (Get it from https://api.fanyi.baidu.com/api/trans/product/index)
            secret_key: Baidu Translate API's secret key (Get it from https://api.fanyi.baidu.com/api/trans/product/index)
            original_language: Original language
            target_language: Target language
        Returns: Translated text
        """
        class fake_http_client_http_connection:
            def __init__(self, *args, **kwargs):
                pass

            def close(self, *args, **kwargs):
                pass
        trans_result = None
        salt = random.randint(32768, 65536)
        sign = hashlib.md5(
            (str(appid)+text+str(salt)+secret_key).encode()).hexdigest()
        targetURL = "https://api.fanyi.baidu.com/api/trans/vip/translate"+"?appid=" + \
            str(appid)+"&q="+urllib.parse.quote(text)+"&from="+original_language + \
            "&to="+target_language+"&salt="+str(salt)+"&sign="+sign
        http_client = fake_http_client_http_connection()
        # Establish a session and return results
        try:
            http_client = http.client.HTTPConnection("api.fanyi.baidu.com")
            http_client.request("GET", targetURL)
            # response is HTTPResponse object
            response = http_client.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            trans_result = result["trans_result"][0]["dst"]
        except Exception as err:
            logger.critical(repr(err))
            msgbox.showerror(
                message=f"An error occurred on the server. Translation is not possible.\nFor details about the error message go to the log of this day. (in \"/logs/{datetime.date.today()}.log\")", title="Translator")
        finally:
            if http_client:
                http_client.close()
                return trans_result
        return None

    def JSONtoXML(json_file_path: str, xml_file_path: str):
        """
        Convert JSON file to XML file
        Args:
            json_file_path: JSON file path
            xml_file_path: XML file path
        Returns :
            0 => Success
            1 => JSON file not found
            2 => JSON file read failure
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
            msgbox.showerror(message="JSON file not found!",
                             title="JSON to XML")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="JSON file read failure!",
                             title="JSON to XML")
            return 2

    def XMLtoJSON(xml_file_path: str, json_file_path: str):
        """
        Convert XML file to JSON file.
        Args:
            xml_file_path: XML file path
            json_file_path: JSON file path
        Returns :
            0 => Success
            1 => XML file not found
            2 => XML file read failure
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
            logger.error("XML file not found: {}".format(xml_file_path))
            msgbox.showerror(message="XML file not found!",
                             title="XML to JSON")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="XML file read failure!",
                             title="XML to JSON")
            return 2

    def CSVtoJSON(csv_file_path: str, json_file_path: str):
        """
        Convert CSV file to JSON file
        Args:
            csv_file_path: CSV file path
            json_file_path: JSON file path
        Returns :
            0 => Success
            1 => CSV file not found
            2 => CSV file read failure
        """
        try:
            with open(csv_file_path, "r", encoding="utf-8") as csv_file:
                csv_data = csv_file.read().splitlines()
                json_data = {}
                for i in range(len(csv_data)):
                    json_data[f"line-{str(i+1)}"] = csv_data[i].split(",")
                with open(json_file_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json.dumps(
                        json_data, ensure_ascii=False, indent=4))
                    return 0
        except FileNotFoundError:
            logger.error("CSV file not found: {}".format(csv_file_path))
            msgbox.showerror(message="CSV file not found!",
                             title="CSV to JSON")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="CSV file read failure!",
                             title="CSV to JSON")
            return 2

    def JSONtoCSV(json_file_path: str, csv_file_path: str):
        """
        Convert JSON file to CSV file.
        Args:
            json_file_path: JSON file path
            csv_file_path: CSV path
        Returns :
            0 => Success
            1 => JSON file not found
            2 => JSON file read failure
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
            msgbox.showerror(message="JSON file not found!",
                             title="JSON to CSV")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="JSON read failure!", title="JSON to CSV")
            return 2

    def getIP(domain=socket.gethostname()):
        """
        Get IP address from domain name
        Args:
            domain: Domain name
        Returns :
            IP address
        """
        try:
            return socket.gethostbyname(domain)
        except socket.error as err:
            return repr(err)

    def resolveDomain(ip):
        """
        Get domain name from IP address
        Args:
            ip: IP address
        Returns :
            Domain name
        """
        try:
            domain = socket.gethostbyaddr(ip)
            return domain[0]
        except socket.error as err:
            return repr(err)

    class FileDiffTools():
        def __init__(self):
            text1 = self.readFromFile(fdg.askopenfilename(
                title="Choose file1", filetypes=(("Plain Text", "*.txt"), ("All Files", "*.*"))))
            text2 = self.readFromFile(fdg.askopenfilename(
                title="Choose file2", filetypes=(("Plain Text", "*.txt"), ("All Files", "*.*"))))
            result = self.diffTexts(text1, text2, fdg.asksaveasfilename(
                title="Save as...", filetypes=(("HTML Files", "*.html"), ("All Files", "*.*"))))
            logger.info("Save file successfully!")
            if result == 0:
                msgbox.showinfo(title="Infomation",
                                message="Save file successfully!")
            else:
                msgbox.showerror(
                    title="Error", message="Save file does not successfully!\nExit code: {}".format(result))

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
            Compare two pieces of text and save the result to an HTML file.
            Args:
                text1: Text 1
                text2: Text 2
                fpath: The path to the saved html file
            Returns: Exit code
                0: Success
                1: Params error
                2: File read failure
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
        msgbox.showerror(
            title="Error", message="Call error! Please call the children of this class.")
        logger.error("Invocation error")

    def charPicture(filename):
        """
        Create a character picture from a picture file.
        Args:
            filename: Picture file path
        """
        color = "MNHQ$OC?7>!:-;."  # Characters

        def to_html(func):
            html_head = '''
                    <html>
                        <head>
                            <style type="text/css">
                                body {font-family:Monospace; font-size:5px;}
                            </style>
                        </head>
                    <body> '''
            html_tail = "</body></html>"
            # Define HTML

            def wrapper(img):
                pic_str = func(img)
                pic_str = "".join(line + " <br/>" for line in pic_str.splitlines())
                return html_head + pic_str + html_tail
            return wrapper
        # Draw character picture

        @to_html
        def make_char_img(img):
            pix = img.load()
            pic_str = ""
            width, height = img.size
            for h in range(height):
                for w in range(width):
                    pic_str += color[int(pix[int(w), int(h)] * 14 / 255)]
                pic_str += "\n"
            return pic_str

        def preprocess(img_name):
            img = Image.open(img_name)
            w, h = img.size
            m = max(img.size)
            delta = m / 200.0
            w, h = int(w / delta), int(h / delta)
            img = img.resize((w, h))
            img = img.convert('L')
            return img

        def save_to_file(filename, pic_str):
            with open(filename, 'w') as outfile:
                logger.debug("File was successfully saved")
                outfile.write(pic_str)
        img = preprocess(filename)
        pic_str = make_char_img(img)
        save_to_file(f"{filename}-char.html", pic_str)
        logger.info(f"Output file: {filename}-char.html")
        msgbox.showinfo(title="Output Success",
                        message="The file has been exported to the same level directory as the image!")

    def bingPicture(fname: str, idx: str = "0", mkt: str = "zh-cn"):
        """
        Get Bing's daily graph
        Args:
            fname: The name of the saved file
            idx: Time:
                0: today
                -1: tommorow
                1: yesterday
                2: the day before yesterday
                3~7 analogy
            mkt: Region. Use the Microsoft region code. e.g. zh-cn: Chinese mainland, en-us: America, etc.
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
                        data = "https://cn.bing.com"+data["images"][0]["url"]
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
        msgbox.showerror(
            title="Error", message="Call error! Please call the children of this class.")
        logger.error("Invocation error")

    class DevToolsLauncher():
        def __init__(self):
            msgbox.showerror(
                title="Error", message="Call error! Please call the children of this class.")
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
                msg="Input URL (bring \"https://\" on)", title="Python Utilities", default=record)
            logger.info(f"User input: {url}")
            if (url != None):
                record = url
                if not (settings["no-log-file"]):
                    with open("logs/records.log", "a") as record_log:
                        record_log.write(f"\n{record}")
            if (url != None):
                global DevTools
                result = DevTools.webConnectTest(url)
                error_list = {1: "Missing protocol", 2: "Server error"}
                if not (1 == result or 2 == result):
                    logger.info(f"Web address connect info: {url} => {result}")
                    msgbox.showinfo(title="Python Utilties", message=result)
                else:
                    msgbox.showinfo(title="Python Utilties",
                                    message=error_list[result-1])

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
                    message="Baidu translate requires your APPID and SecretKey to use. OK to input?\nTranslator promises never to compromise your privacy.", title="Translator", icon="warning")
                if result:
                    datas = easygui.multpasswordbox(
                        "Input AppID and SecretKey.", title="Translator", fields=["AppID", "SecretKey"])
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
            if (entered == True):
                with open("./data/translator.languages.json", "r") as languages:
                    languages = languages.read()
                    languages = json.loads(languages)
                global DevTools
                text = easygui.enterbox(
                    "Input text to translate.", title="Translator", default="None")
                if text:
                    fromLang = "auto"
                    toLang = easygui.choicebox("What language do you want to output?", choices=list(
                        languages.keys()), title="Translator")
                    logger.info(
                        f"User input: [{text}, {fromLang}, {languages[toLang]}]")
                    if (text != None) and (fromLang != None) and (toLang != None):
                        result = DevTools.translator(
                            text, id, key, fromLang, languages[toLang])
                        msgbox.showinfo(
                            message=f"Translation complete\nOriginal: {text}\nResult: {result}\nLanguage: {toLang}\n", title="Translator")
                        logger.info(f"Result: {result}")
                    else:
                        msgbox.showerror(
                            message="Parameters are missing!", title="Translator")
                        logger.error("Missing arguments")

        @staticmethod
        def JSONtoXMLLauncher():
            json = easygui.fileopenbox(title="Open...", filetypes=[
                                       ["*.json", "JSON files"]], default="*.json")
            xml = easygui.filesavebox(title="Save As...", filetypes=[
                                      ["*.xml", "XML files"]], default="*.xml")
            if (json != None):
                if (os.path.splitext(json)[-1] == ".json"):
                    global DevTools
                    logger.info(f"Input JSON: {json}")
                    DevTools.JSONtoXML(json, xml)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(
                        title="ERROR", message="the file extension is not \".json\"!")
                    logger.error("File extension is incorrect")

        @staticmethod
        def XMLtoJSONLauncher():
            xml = easygui.fileopenbox(title="Open...", filetypes=[
                                      ["*.xml", "XML files"]], default="*.xml")
            json = easygui.filesavebox(title="Save As...", filetypes=[
                                       ["*.json", "JSON files"]], default="*.json")
            if (xml != None):
                if (os.path.splitext(xml)[-1] == ".xml"):
                    global DevTools
                    logger.info(f"Input XML:{xml}")
                    DevTools.XMLtoJSON(xml, json)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(
                        title="Error", message="The file extension is not \".xml\"!")
                    logger.error("File extension is incorrect")

        @staticmethod
        def getIPLauncher():
            global DevTools
            ip = easygui.enterbox(
                "Enter the domain name or enter '@default' to use local domain name", title="IP address getter")
            if (ip != None):
                if (ip != "@default"):
                    global DevTools
                    logger.info(f"Input IP:{ip}")
                    result = DevTools.getIP(ip)
                    msgbox.showinfo(
                        message=f"IP address: {result}", title="IP address getter")
                    logger.info(f"Result: {result}")
                else:
                    logger.info(f"Input IP:{ip}")
                    result = DevTools.getIP()
                    msgbox.showinfo(
                        message=f"IP address: {result}", title="IP address getter")
                    logger.info(f"Result: {result}")

        @staticmethod
        def resolveDomainLauncher():
            domain = easygui.enterbox(
                "Enter the IP address", title="DNS resolver")
            if (domain != None):
                global DevTools
                logger.info(f"Input Domain:{domain}")
                result = DevTools.resolveDomain(domain)
                msgbox.showinfo(
                    message=f"Resolution result: {result}", title="DNS resolver")
                logger.info(f"Result:{result}")

        @staticmethod
        def JSONtoCSVLauncher():
            json = easygui.fileopenbox(title="Open...", filetypes=[
                                       ["*.json", "JSON files"]], default="*.json")
            csv = easygui.filesavebox(title="Save as...", filetypes=[
                                      ["*.csv", "CSV files"]], default="*.csv")
            if (json != None):
                if (os.path.splitext(json)[-1] == ".json"):
                    global DevTools
                    logger.info(f"Input JSON:{json}")
                    DevTools.JSONtoCSV(json, csv)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(
                        title="Error", message="File extension is not \".json\"!")
                    logger.error("File extension is incorrect")

        @staticmethod
        def CSVtoJSONLauncher():
            csv = easygui.fileopenbox(title="Open...", filetypes=[
                                      ["*.csv", "CSV files"]], default="*.csv")
            json = easygui.filesavebox(title="Save as...", filetypes=[
                                       ["*.json", "JSON files"]], default="*.json")
            if (csv != None):
                if (os.path.splitext(csv)[-1] == ".csv"):
                    global DevTools
                    logger.info(f"Input CSV:{csv}")
                    DevTools.CSVtoJSON(csv, json)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(
                        title="Error", message="File extension is not \".csv\"！")
                    logger.error("File extension is incorrect")

    class DrawingToolsLauncher():
        def __init__(self):
            msgbox.showerror(
                title="Error", message="Call error! Please call the children of this class.")
            logger.error("Invocation error")

        @staticmethod
        def charPictureLauncher():
            path = easygui.fileopenbox(title="Open...", filetypes=[
                                       ["*.jpg", "*.jpeg", "JPG files"], ["*.bmp", "BMP files"], ["*.gif", "GIF files"]], default="*.png")
            if (path != None):
                if (os.path.splitext(path)[-1] == ".png") or (os.path.splitext(path)[-1] == ".jpg") or (os.path.splitext(path)[-1] == ".bmp") or (os.path.splitext(path)[-1] == ".gif") or (os.path.splitext(path)[-1] == ".jpeg"):
                    global DrawingTools
                    logger.info(f"Input picture:{path}")
                    DrawingTools.charPicture(path)
                else:
                    msgbox.showerror(
                        title="Error", message="The file extension is incorrect!")
                    logger.error("File extension is incorrect")

        @staticmethod
        def bingPictureLauncher():
            fname = fdg.asksaveasfilename(title="Save as...", filetypes=[
                                          ["JPG Files", "*.jpg"]], defaultextension="*.jpg")
            if (fname != None):
                logger.info(f"Input path: {fname}")
                if (os.path.splitext(fname)[-1] == ".jpg"):
                    params = easygui.multenterbox(
                        title="Bing Picture", msg="Please enter the infomations", fields=["Index", "Region Code"])
                    if (params != None != ["", "", ""]):
                        if (params[0].isdigit()) or (params[0] == "-1"):
                            params.insert(0, fname)
                            logger.info(f"Input params:{params}")
                            global DrawingTools
                            DrawingTools.bingPicture(
                                params[0], params[1], params[2])
                            logger.info("Done.")
                            msgbox.showinfo(
                                title="Infomation", message="The image has been saved to the specified path.")
                        else:
                            msgbox.showerror(
                                title="Error", message="The index must be a number!")
                            return
                else:
                    logger.error("File extension is incorrect")
                    msgbox.showerror(
                        title="Error", message="File extension is incorrect!")
                    return

    class ExternalLauncher():
        def __init__(self):
            msgbox.showerror(
                title="Error", message="Call error! Please call the children of this class.")
            logger.error("Invocation error")

        @staticmethod
        def webSpeedTsetLauncher():
            def run():
                subprocess.Popen("python src/webspeedtest/main.py")
            msgbox.showwarning(title="Warning", message="The waiting time of this program is extremely long about 2 minutes and the speed test operation will be performed in the background.\nYou can still use this program normally while waiting")
            thread = threading.Thread(target=run)
            thread.start()

        @staticmethod
        def clockLauncher():
            # python "src\clock\main.py"
            subprocess.Popen("python src/clock/main.py")

        @staticmethod
        def calculatorLauncher():
            subprocess.Popen("python src/calculator/main.py")

        @staticmethod
        def md5CheckerLauncher():
            msgbox.showinfo(title="Python Utilities",
                            message="MD5 Checker in \"src\\cmdtools\\md5.py\". Follow the prompts to use, please.")

        @staticmethod
        def passwordCreatorLauncher():
            # python "src\passwordCreator\main.py"
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
        def captchaLauncher():
            subprocess.Popen("python src/Captcha_Generator/main.py")

        @staticmethod
        def easyToDoLauncher():
            subprocess.Popen("python src/EasyTodo/main.py")


class System():
    @staticmethod
    def about():
        msgbox.showinfo(title="Python Utilities", message="""Python Utilities v2.11.0 en-US
Author: @wangzixin1940
Current File: release/en-US/main.py
README File：README.md
GNU GPLv3 License：https://github.com/wangzixin1940/Python-Utilities/blob/main/LICENCE
VERSION 2.11 RELEASE
""")

    @staticmethod
    def languageSettings():
        subprocess.Popen("python ../../main.py")
        root.destroy()

    @staticmethod
    def quitApp():
        root.destroy()

    def switchTheme(theme_name):
        if (theme_name == "pride"):
            root.iconbitmap("./images/pride.ico")
            style.theme_use("cosmo")
            style.configure("TButton", font=(
                "等线 Light", 18, "normal"), width=20, height=3)
            style.configure("TMenubutton", font=(
                "等线 Light", 18, "normal"), width=19, height=3)
        else:
            root.iconbitmap("./images/icon.ico")
            style.theme_use(theme_name)
            style.configure("TButton", font=(
                "等线 Light", 18, "normal"), width=20, height=3)
            style.configure("TMenubutton", font=(
                "等线 Light", 18, "normal"), width=19, height=3)
        theme["theme"] = theme_name
        with open("./data/theme.json", "w") as f:
            json.dump(theme, f)

    @staticmethod
    def importSettings():
        path = easygui.fileopenbox(title="Open...", filetypes=[
                                   ["*.json", "JSON files"]], default="*.json")
        global settings
        if (path != None):
            if (msgbox.askokcancel(title="Python Utilities", message="OK to import?\nThe existing configuration file will be overwritten.\nA corrupted configuration file may cause the program to run incorrectly.", icon="warning")):
                with open(path, "r+", encoding="utf-8") as new_settings:
                    new_settings = new_settings.read()
                    new_settings = json.loads(new_settings)
                    logger.info(f"Settings: {new_settings}")
                    with open("data/settings.json", "w+", encoding="utf-8") as settings:
                        settings.write(json.dumps(
                            new_settings, ensure_ascii=False, indent=4))
                        msgbox.showinfo(title="Python Utilities",
                                        message="Settings imported successfully!")
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
                "Ccon file not found. Program will use default icon and cosmo theme.")
    style.configure("TButton", font=("Times New Roman",
                    14, "normal"), width=30, height=3)
    style.configure("TMenubutton", font=(
        "Times New Roman", 14, "normal"), width=28, height=3)
    # Window
    # ===================================== #
    title = ttk.Label(root, text="Python Utilities",
                      font=("Airal", 20, "bold"))
    title.pack()  # Title
    # ===================================== #
    utilitiesLabel = ttk.Label(
        root, text="Utilities 🛠", font=("Airal", 18, "normal"))
    utilitiesLabel.pack()  # Utilities tab
    translateButton = ttk.Button(
        text="Translator", command=Launcher.DevToolsLauncher.translatorLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    translateButton.pack()  # Translator button
    weatherButton = ttk.Button(text="Weather forecast",
                               command=Launcher.ExternalLauncher.weatherLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    weatherButton.pack()  # Weather forecast button
    speech2textButton = ttk.Button(
        text="Speech to text", command=Launcher.ExternalLauncher.speech2textLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speech2textButton.pack()  # Speech to text button
    easyToDoButton = ttk.Button(root, text="Easy To Do", command=Launcher.ExternalLauncher.easyToDoLauncher,
                                bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    easyToDoButton.pack()  # Easy To Do Button
    # ===================================== #
    DevToolsLabel = ttk.Label(
        root, text="DevTools </>", font=("Airal", 18, "normal"))
    DevToolsLabel.pack()  # DevTools tab
    connectButton = ttk.Button(text="Detect website status code",
                               command=Launcher.DevToolsLauncher.webConnectTestLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    connectButton.pack()  # Check website status code button
    speedTestButton = ttk.Button(
        text="Web Speed Test", command=Launcher.ExternalLauncher.webSpeedTsetLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speedTestButton.pack()  # SpeedTest button
    # ===================================== #
    externalsLabel = ttk.Label(
        root, text="Other Tools 🧰", font=("Airal", 18, "normal"))
    externalsLabel.pack()  # Other tools tab
    passwordCreatorButton = ttk.Button(
        text="Password Creator", command=Launcher.ExternalLauncher.passwordCreatorLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    passwordCreatorButton.pack()  # Password creator button
    # ===================================== #
    if not (settings["no-menu"]):
        menu = ttk.Menu(root)
        fileMenu = ttk.Menu(menu)
        otherMenu = ttk.Menu(menu)
        settingsMenu = ttk.Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        menu.add_cascade(label="Other", menu=otherMenu)
        if not (settings["no-settings-menu"]):
            menu.add_cascade(label="Settings", menu=settingsMenu)
        menu.add_command(label="About", command=System.about)
        fileMenu.add_command(label="Import settings...", command=System.importSettings)
        fileMenu.add_command(label="Exit", command=System.quitApp)
        otherMenu.add_command(
            label="Calculator", command=Launcher.ExternalLauncher.calculatorLauncher)
        otherMenu.add_command(
            label="Hash Checker", command=Launcher.ExternalLauncher.md5CheckerLauncher)
        otherMenu.add_command(
            label="Licence Creator", command=Launcher.ExternalLauncher.licenceCreatorLauncher)
        otherMenu.add_command(
            label="Send mail from JSON", command=Launcher.ExternalLauncher.sendMailFromJSONLauncher)
        ipToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="IP tools", menu=ipToolsMenu)
        ipToolsMenu.add_command(
            label="Get IP", command=Launcher.DevToolsLauncher.getIPLauncher)
        ipToolsMenu.add_command(
            label="Resolve doamin", command=Launcher.DevToolsLauncher.resolveDomainLauncher)
        fileToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="File tools", menu=fileToolsMenu)
        fileToolsMenu.add_command(
            label="JSON to XML", command=Launcher.DevToolsLauncher.JSONtoXMLLauncher)
        fileToolsMenu.add_command(
            label="XML to JSON", command=Launcher.DevToolsLauncher.XMLtoJSONLauncher)
        fileToolsMenu.add_command(
            label="JSON to CSV", command=Launcher.DevToolsLauncher.JSONtoCSVLauncher)
        fileToolsMenu.add_command(
            label="CSV to JSON", command=Launcher.DevToolsLauncher.CSVtoJSONLauncher)
        fileToolsMenu.add_command(
            label="File diff", command=DevTools.FileDiffTools)
        qrcodeToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="QR Code tools", menu=qrcodeToolsMenu)
        qrcodeToolsMenu.add_command(
            label="QRCode Generator", command=Launcher.ExternalLauncher.qrcodeGeneratorLauncher)
        qrcodeToolsMenu.add_command(
            label="QRCode Parser", command=Launcher.ExternalLauncher.qrcodeParserLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(
            label="ASCII Art", command=Launcher.DrawingToolsLauncher.charPictureLauncher)
        otherMenu.add_command(
            label="Bing's daily picture", command=Launcher.DrawingToolsLauncher.bingPictureLauncher)
        otherMenu.add_command(
            label="Picture format convertor", command=Launcher.ExternalLauncher.pictureFormatConverterLauncher)
        otherMenu.add_command(
            label="Auto mouse and keyboard", command=Launcher.ExternalLauncher.AMKLauncher)
        otherMenu.add_command(
            label="Generate a verification code (incomplete)", command=Launcher.ExternalLauncher.captchaLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(
            label="Clock", command=Launcher.ExternalLauncher.clockLauncher)
        otherMenu.add_command(
            label="Count down timer", command=Launcher.ExternalLauncher.countDownLauncher)
        otherMenu.add_command(
            label="Chinese Pinyin Dictionary (Only available in Chinese version)", state="disabled")
        if not (settings["no-settings-menu"]):
            themesMenu = ttk.Menu(settingsMenu)
            settingsMenu.add_cascade(label="Themes...", menu=themesMenu)
            for i in style.theme_names():
                themesMenu.add_radiobutton(
                    label=i, command=lambda name=i: System.switchTheme(name))
            themesMenu.add_separator()
            themesMenu.add_command(
                label="pride", command=lambda: System.switchTheme("pride"))
            settingsMenu.add_command(
                label="切换到简体中文...", command=System.languageSettings)
        root.config(menu=menu)
    # Tools tab
    # ===================================== #
    root.mainloop()


if __name__ == '__main__':
    logger.info("Platform: {system} {version}".format(
        system=sysinfo["system"], version=sysinfo["version"]))
    logger.info("Python: {version} {implementation}".format(
        version=sysinfo["python"]["version"], implementation=sysinfo["python"]["implementation"]))
    # Output system info
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
