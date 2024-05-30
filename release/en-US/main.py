import json

with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read settings.json

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding=settings["encoding"])
# Change encoding to settings["encoding"]

import os
os.chdir(os.path.dirname(__file__))
# Change current directory to the script's directory

# Reserved modules
from tkinter import messagebox as msgbox
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import easygui
import logging
import datetime
import platform

# Modules required for the tool
import requests
from PIL import Image
import os
import http.client
import hashlib
import urllib
import random
import subprocess
import threading
import xmltodict
import dicttoxml
import socket

if not(settings["no-log-file"]):
    logging.basicConfig(
                    filename=f"./logs/{datetime.date.today()}.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
    )
else :
    logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - NO-LOG-FILE - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
    )
logger = logging.getLogger("ROOT")
# print(logger.__dict__)
# Configure log information

sysinfo = {
    "system" : platform.system(),
    "version" : platform.version(),
    "python": {
        "version": platform.python_version().split("."),
        "implementation": platform.python_implementation(),
    }
}
for i in range(len(sysinfo["python"]["version"])): sysinfo["python"]["version"][i] = int(sysinfo["python"]["version"][i])

class DevTools():
    def __init__(self):
        msgbox.showerror(title="Error", message="Call error! Please call the children of this class.")
        logger.error("INVOCATION ERROR")
    def webConnectTest(url:str):
        """
        Test if the website is accessible
        url: website URL
        """
        try :
            result = str(requests.get(url).status_code)
        except requests.exceptions.MissingSchema as err:
            logger.critical("MISSING SCHEMA ERROR")
            return 1
        # Return http status code
        # print(result)
        with open("./data/connect.test.codes.json", "r") as statusCodes:
            statusCodes = statusCodes.read()
            statusCodes = json.loads(statusCodes)
        # A list of common http status codes
        try :
            return str(result) + "：" + statusCodes[result]
        except KeyError:
            logger.error(f"STATUS CODE:{result} NOT FOUND")
            return 2
        # If the http status code is known, the result is returned. Otherwise the user is prompted to return an unknown status code
    def translator(text:str, appid:str, secretKey:str, originalLanguage:str, targetLanguage:str):
        """
        text: Texts that need to be translated
        appid: Baidu Translate API's appid (Get it from https://api.fanyi.baidu.com/api/trans/product/index)
        secretKey: Baidu Translate API's secretKey (Get it from https://api.fanyi.baidu.com/api/trans/product/index)
        originalLanguage: Original language
        targetLanguage: Target language
        return：Translated text
        """
        salt = random.randint(32768, 65536)
        sign = hashlib.md5((str(appid)+text+str(salt)+secretKey).encode()).hexdigest()
        targetURL = "http://api.fanyi.baidu.com/api/trans/vip/translate"+"?appid="+str(appid)+"&q="+urllib.parse.quote(text)+"&from="+originalLanguage+"&to="+targetLanguage+"&salt="+str(salt)+"&sign="+sign
        httpClient = None
        # Establish a session and return results
        try:
            httpClient = http.client.HTTPConnection("api.fanyi.baidu.com")
            httpClient.request("GET", targetURL)
            # response is HTTPResponse object
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            trans_result = result["trans_result"][0]["dst"]
        except Exception as err:
            logger.critical(repr(err))
            msgbox.showerror(message=f"An error occurred on the server. Translation is not possible.\nFor details about the error message go to the log of this day. (in \"/logs/{datetime.date.today()}.log\")", title="Translator")
        finally:
            if httpClient:
                httpClient.close()
                return trans_result
        return None
    def JSONtoXML(json_file_path:str, xml_file_path:str):
        """
        json_file_path: JSON file path
        xml_file_path: XML file path
        return :
            0 => Success
            1 => JSON file not found
            2 => JSON file read failure
        """
        try :
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)
                xml_data = str(dicttoxml.dicttoxml(json_data))
                with open(xml_file_path, "w", encoding="utf-8") as xml_file:
                    xml_file.write(xml_data)
                    return 0
        except FileNotFoundError:
            logger.error("JSON FILE NOT FOUND: {}".format(json_file_path))
            msgbox.showerror(message="JSON file not found!", title="JSON to XML")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="JSON file read failure!", title="JSON to XML")
            return 2
    def XMLtoJSON(xml_file_path:str, json_file_path:str):
        """
        xml_file_path: XML file path
        json_file_path: JSON file path
        return :
            0 => Success
            1 => XML file not found
            2 => XML file read failure
        """
        try :
            with open(xml_file_path, "r", encoding="utf-8") as xml_file:
                xml_data = xml_file.read()
                json_data = json.dumps(xmltodict.parse(xml_data), ensure_ascii=False)
                with open(json_file_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json_data)
                    return 0
        except FileNotFoundError:
            logger.error("XML FILE NOT FOUND: {}".format(xml_file_path))
            msgbox.showerror(message="XML file not found!", title="XML to JSON")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="XML file read failure!", title="XML to JSON")
            return 2
    def getIP(domain=socket.gethostname()):
        """
        domain: Domain name
        return :
            IP address
        """
        try :
            return socket.gethostbyname(domain)
        except socket.error as err:
            return repr(err)
    def resolveDomain(ip):
        """
        ip: IP address
        return :
            Domain name
        """
        try:
            domain = socket.gethostbyaddr(ip)
            return domain[0]
        except socket.error as err:
            return repr(err)


class DrawingTools():
    def __init__(self):
        msgbox.showerror(title="Error", message="Call error! Please call the children of this class.")
        logger.error("INVOCATION ERROR")
    def charPicture(filename):
        """
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
                pic_str = "".join(l + " <br/>" for l in pic_str.splitlines())
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
                logger.debug("FILE WAS SUCCESSFULLY SAVED")
                outfile.write(pic_str)
        img = preprocess(filename)
        pic_str = make_char_img(img)
        save_to_file(f"{filename}-char.html", pic_str)
        logger.info(f"OUTPUT FILE:{filename}-char.html")
        msgbox.showinfo(title="Output Success", message="The file has been exported to the same level directory as the image!")

class Launcher():
    def __init__(self):
        msgbox.showerror(title="Error", message="Call error! Please call the children of this class.")
        logger.error("INVOCATION ERROR")
    class DevToolsLauncher():
        def __init__(self):
            msgbox.showerror(title="Error", message="Call error! Please call the children of this class.")
            logger.error("INVOCATION ERROR")
        def webConnectTestLauncher():
            try :
                with open("logs/records.log", "r") as r:
                    try :
                        record = r.readlines()[len(r.readlines()) - 1]
                    except IndexError:
                        record = ""
            except FileNotFoundError:
                record = ""
            url = easygui.enterbox(msg="Input URL (bring \"http://\" on)", title="Windows Utilties", default=record)
            logger.info(f"USER INPUT:{url}")
            if (url != None):
                record = url
                if not(settings["no-log-file"]):
                    with open("logs/records.log", "a") as record_log:
                        record_log.write(f"\n{record}")
            if (url != None):
                global DevTools
                result = DevTools.webConnectTest(url)
                error_list = {1:"Missing protocol", 2:"Server error"}
                if not(1 == result or 2 == result):
                    logger.info(f"WEB ADDRESS CONNECT INFO: {url} => {result}")
                    msgbox.showinfo(title="Windows Utilties", message=result)
                else :
                    msgbox.showinfo(title="Windows Utilties", message=error_list[result-1])
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
                result = msgbox.askokcancel(message="Baidu translate requires your APPID and SecretKey to use. OK to input?\nTranslator promises never to compromise your privacy.", title="Translator", icon="warning")
                if result == True:
                    datas = easygui.multpasswordbox("Input AppID and SecretKey.", title="Translator", fields=["AppID", "SecretKey"])
                    if datas != None:
                        id = datas[0]
                        key = datas[1]
                        entered = True
                        with open("data/translator.appid.json", "w") as appid:
                            appid.write(json.dumps({"id":id, "key":key}))
                    else :
                        entered = False
                else :
                    entered = False
            if (entered == True):
                with open("./data/translator.languages.json", "r") as languages:
                    languages = languages.read()
                    languages = json.loads(languages)
                global DevTools
                text = easygui.enterbox("Input text to translate.", title="Translator", default="None")
                if text:
                    fromLang = "auto"
                    toLang = easygui.choicebox("What language do you want to output?", choices=list(languages.keys()), title="Translator")
                    # print(languages.keys())
                    logger.info(f"USER INPUT:[{text}, {fromLang}, {languages[toLang]}]")
                    if (text != None)and(fromLang != None)and(toLang != None):
                        result = DevTools.translator(text, id, key, fromLang, languages[toLang])
                        msgbox.showinfo(message=f"Translation complete\nOriginal: {text}\nResult: {result}\nLanguage: {toLang}\n", title="Translator")
                        logger.info(f"RESULT:{result}")
                    else :
                        msgbox.showerror(message="Parameters are missing!", title="Translator")
                        logger.error("MISSING ARGUMENTS")
        def JSONtoXMLLauncher():
            json = easygui.fileopenbox(title="Open...", filetypes=[["*.json", "JSON files"]], default="*.json")
            xml = easygui.filesavebox(title="Save As...", filetypes=[["*.xml", "XML files"]], default="*.xml")
            if (json != None):
                if (os.path.splitext(json)[-1] == ".json"):
                    global DevTools
                    logger.info(f"INPUT JSON:{json}")
                    DevTools.JSONtoXML(json, xml)
                    logger.info(f"OUTPUT FINISH")
                else :
                    msgbox.showerror(title="ERROR", message="the file extension is not \".json\"!")
                    logger.error("FILE EXTENSION IS INCORRECT")
        def XMLtoJSONLauncher():
            xml = easygui.fileopenbox(title="Open...", filetypes=[["*.xml", "XML files"]], default="*.xml")
            json = easygui.filesavebox(title="Save As...", filetypes=[["*.json", "JSON files"]], default="*.json")
            if (xml != None):
                if (os.path.splitext(xml)[-1] == ".xml"):
                    global DevTools
                    logger.info(f"INPUT XML:{xml}")
                    DevTools.XMLtoJSON(xml, json)
                    logger.info(f"OUTPUT FINISH")
                else :
                    msgbox.showerror(title="Error", message="The file extension is not \".xml\"!")
                    logger.error("FILE EXTENSION IS INCORRECT")
        def getIPLauncher():
            ip = easygui.enterbox("Enter the domain name or enter '@default' to use local domain name", title="IP address getter")
            if (ip != None):
                if (ip != "@default"):
                    global DevTools
                    logger.info(f"INPUT IP:{ip}")
                    result = DevTools.getIP(ip)
                    msgbox.showinfo(message=f"IP address: {result}", title="IP address getter")
                    logger.info(f"RESULT:{result}")
                else :
                    logger.info(f"INPUT IP:{ip}")
                    result = DevTools.getIP()
                    msgbox.showinfo(message=f"IP address: {result}", title="IP address getter")
                    logger.info(f"RESULT:{result}")
        def resolveDomainLauncher():
            domain = easygui.enterbox("Enter the IP address", title="DNS resolver")
            if (domain != None):
                global DevTools
                logger.info(f"INPUT DOMAIN:{domain}")
                result = DevTools.resolveDomain(domain)
                msgbox.showinfo(message=f"Resolution result: {result}", title="DNS resolver")
                logger.info(f"RESULT:{result}")

    class DrawingToolsLauncher():
        def __init__(self):
            msgbox.showerror(title="Error", message="Call error! Please call the children of this class.")
            logger.error("INVOCATION ERROR")
        def charPictureLauncher():
            path = easygui.fileopenbox(title="Open...", filetypes=[["*.jpg", "*.jpeg" , "JPG files"], ["*.bmp", "BMP files"], ["*.gif", "GIF files"]], default="*.png")
            if (path != None):
                if (os.path.splitext(path)[-1] == ".png")or(os.path.splitext(path)[-1] == ".jpg")or(os.path.splitext(path)[-1] == ".bmp")or(os.path.splitext(path)[-1] == ".gif")or(os.path.splitext(path)[-1] == ".jpeg"):
                    global DrawingTools
                    logger.info(f"INPUT PICTURE:{path}")
                    DrawingTools.charPicture(path)
                else :
                    msgbox.showerror(title="Error", message="The file extension is incorrect!")
                    logger.error("FILE EXTENSION IS INCORRECT")
    class ExternalLauncher():
        def __init__(self):
            msgbox.showerror(title="Error", message="Call error! Please call the children of this class.")
            logger.error("INVOCATION ERROR")
        def webSpeedTsetLauncher():
            def run():
                subprocess.Popen("python ./src/webspeedtest/main.py")
            msgbox.showwarning(title="Warning", message="The waiting time of this program is extremely long about 2 minutes and the speed test operation will be performed in the background.\nYou can still use this program normally while waiting")
            thread = threading.Thread(target=run)
            thread.start()
        def clockLauncher():
            subprocess.Popen("python \"src\\clock\\main.py\"") # python "src\clock\main.py"
        def calculatorLauncher():
            subprocess.Popen("calc")
        def md5CheckerLauncher():
            msgbox.showinfo(title="Windows Utilities", message="MD5 Checker in \"src\\cmdtools\\md5.py\". Follow the prompts to use, please.")
        def passwordCreatorLauncher():
            subprocess.Popen("python \"src\\passwordCreator\\main.py\"") # python "src\passwordCreator\main.py"
        def licenceCreatorLauncher():
            subprocess.Popen("python src/licenceCreator/main.py")

class System():
    def about():
        msgbox.showinfo(title="Windows Utilities", message="""Windows Utilities v1.11.5 en-US
Author: @wangzixin1940
Editor: Microsoft Visual Studio Code
Current File: main.py
Release Date: 2024-5-19
README File：README.md (en-US and zh-CN)
MIT License：https://github.com/wangzixin1940/Windows-Utilities/blob/main/LICENCE
VERSION 1.11 RELEASE
""")
    def languageSettings():
        msgbox.showinfo(title="Windows 实用工具", message="前往\"../../main.py\"运行中文版本！")
    def quitApp():
        root.destroy()
    def switchTheme():
        if msgbox.askokcancel(title="Windows Utilities", message="OK to change theme?\nYou need to restart the program after the switch to take effect. The program will close automatically when opened.", icon="warning"):
            subprocess.Popen("python \"tools\\configurator.py\"") # python "tools\configurator.py"
            root.destroy()
    def importSettings():
        path = easygui.fileopenbox(title="Open...", filetypes=[["*.json", "JSON files"]], default="*.json")
        global settings
        if (path != None):
            if (msgbox.askokcancel(title="Windows Utilities", message="OK to import?\nThe existing configuration file will be overwritten.\nA corrupted configuration file may cause the program to run incorrectly.", icon="warning")):
                with open(path, "r+", encoding="utf-8") as new_settings:
                    new_settings = new_settings.read()
                    new_settings = json.loads(new_settings)
                    logger.info(f"SETTINGS: {new_settings}")
                    with open("data/settings.json", "w+", encoding="utf-8") as settings:
                        settings.write(json.dumps(new_settings, ensure_ascii=False, indent=4))
                        msgbox.showinfo(title="Windows Utilities", message="Settings imported successfully!")
                        logger.info("SETTINGS IMPORTED")

def main():
    global root
    global style
    root = ttk.Window()
    with open("./data/theme.json", "r", encoding="utf-8") as theme:
        theme = theme.read()
        theme = json.loads(theme)
    logger.info("STARTING APP")
    root.title("Windows Utilities")
    root.geometry("{}x{}".format(settings["geometry"][0], settings["geometry"][1]))
    root.resizable(settings["resizable"][0], settings["resizable"][1])
    if settings["icon-file-path"] == "@default":
        if theme["theme"] == "pride":
            root.iconbitmap("./images/pride.ico")
            style = ttk.Style("cosmo")
        else :
            root.iconbitmap("./images/icon.ico")
            style = ttk.Style(theme["theme"])
    else :
        if os.path.exists(settings["icon-file-path"]):
            root.iconbitmap(settings["icon-file-path"])
            style = ttk.Style("cosmo")
        else :
            root.iconbitmap("./images/icon.ico")
            style = ttk.Style("cosmo")
            logger.warning("ICON FILE NOT FOUND. PROGRAM WILL USE DEFAULT ICON AND COSMO THEME.")
    style.configure("TButton", font=("Times New Roman",14,"normal"), width=30, height=3)
    style.configure("TMenubutton", font=("Times New Roman",14,"normal"), width=28, height=3)
    # Window
    # ===================================== #
    title = ttk.Label(root, text="Windows Utilities", font=("Airal",20,"bold"))
    title.pack() # Title
    # ===================================== #
    utilitiesLabel = ttk.Label(root, text="Utilities 🛠", font=("Airal",18,"normal"))
    utilitiesLabel.pack() # Utilities tab
    translateButton = ttk.Button(root, text="Translator", command=Launcher.DevToolsLauncher.translatorLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    translateButton.pack() # Translator button
    # ===================================== #
    DevToolsLabel = ttk.Label(root, text="DevTools </>", font=("Airal",18,"normal"))
    DevToolsLabel.pack() # DevTools tab
    connectButton = ttk.Button(root, text="Detect website status code", command=Launcher.DevToolsLauncher.webConnectTestLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    connectButton.pack() # Check website status code button
    speedTestButton = ttk.Button(root, text="Web Speed Test",command=Launcher.ExternalLauncher.webSpeedTsetLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speedTestButton.pack() # SpeedTest button
    # ===================================== #
    externalsLabel = ttk.Label(root, text="Other Tools 🧰", font=("Airal",18,"normal"))
    externalsLabel.pack() # Other tools tab
    passwordCreatorButton = ttk.Button(root, text="Password Creator", command=Launcher.ExternalLauncher.passwordCreatorLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    passwordCreatorButton.pack() # Password creator button
    # ===================================== #
    if not(settings["no-menu"]):
        menu = ttk.Menu(root)
        fileMenu = ttk.Menu(menu)
        otherMenu = ttk.Menu(menu)
        settingsMenu = ttk.Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        menu.add_cascade(label="Other", menu=otherMenu)
        if not(settings["no-settings-menu"]):
            menu.add_cascade(label="Settings", menu=settingsMenu)
        menu.add_command(label="About", command=System.about)
        fileMenu.add_command(label="Import settings...", command=System.importSettings)
        fileMenu.add_command(label="Exit", command=System.quitApp)
        otherMenu.add_command(label="Calculator", command=Launcher.ExternalLauncher.calculatorLauncher)
        otherMenu.add_command(label="Check md5", command=Launcher.ExternalLauncher.md5CheckerLauncher)
        otherMenu.add_command(label="Licence Creator", command=Launcher.ExternalLauncher.licenceCreatorLauncher)
        ipToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="IP tools", menu=ipToolsMenu)
        ipToolsMenu.add_command(label="IP address lookup", command=Launcher.DevToolsLauncher.getIPLauncher)
        ipToolsMenu.add_command(label="Reverse IP lookup", command=Launcher.DevToolsLauncher.resolveDomainLauncher)
        fileToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="File tools", menu=fileToolsMenu)
        fileToolsMenu.add_command(label="JSON to XML", command=Launcher.DevToolsLauncher.JSONtoXMLLauncher)
        fileToolsMenu.add_command(label="XML to JSON", command=Launcher.DevToolsLauncher.XMLtoJSONLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(label="Clock", command=Launcher.ExternalLauncher.clockLauncher)
        otherMenu.add_command(label="Character picture", command=Launcher.DrawingToolsLauncher.charPictureLauncher)
        if not(settings["no-settings-menu"]):
            settingsMenu.add_command(label="Themes...", command=System.switchTheme)
            settingsMenu.add_command(label="Language settings...", command=System.languageSettings)
        root.config(menu=menu)
    # Tools tab
    # ===================================== #
    root.mainloop()


if __name__ == '__main__':
    logger.info("Platform: {system} {version}".format(system=sysinfo["system"], version=sysinfo["version"]))
    logger.info("Python: {version} {implementation}".format(version=sysinfo["python"]["version"], implementation=sysinfo["python"]["implementation"]))
    # Output system info
    if sysinfo["python"]["version"][0] >= 3:
        if sysinfo["python"]["version"][1] >= 8:
            main(); exit(0)
        else:
            logger.warning("Python Version too old: {}".format(sysinfo["python"]["version"]))
    else:
        logger.warning("Python Version too old: {}".format(sysinfo["python"]["version"]))
    main(); exit(1)

