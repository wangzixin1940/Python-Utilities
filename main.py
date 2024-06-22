import json

with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # 读取设置文件

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding=settings["encoding"])
# 更换编码

import os
os.chdir(os.path.dirname(__file__))
# 更换工作目录

# 保留模块
from tkinter import messagebox as msgbox
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import easygui
import logging
import datetime
import platform

# 工具所需模块
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
from tkinter.filedialog import asksaveasfilename, askopenfilename
from difflib import HtmlDiff

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
# 配置日志信息

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
        msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
        logger.error("Invocation error")
    def webConnectTest(url:str):
        """
        测试网站是否可以访问
        url: 网站URL
        """
        try :
            result = str(requests.get(url).status_code)
        except requests.exceptions.MissingSchema as err:
            logger.critical("Missing schema error")
            return f"协议不存在，您是否忘记在网站开头加上“http://”？\n{repr(err)}"
        # 返回HTTP状态码
        with open("./data/connect.test.codes.json", "r") as statusCodes:
            statusCodes = statusCodes.read()
            statusCodes = json.loads(statusCodes)
        # 常见的HTTP状态码列表
        try :
            return str(result) + "：" + statusCodes[result]
        except KeyError:
            logger.error(f"Status code: {result} not found")
            return f"网站返回了一个未知的HTTP状态码：{result}"
        # 如果HTTP状态码已知，则返回结果；否则提示用户返回未知状态码
    def translator(text:str, appid:str, secretKey:str, originalLanguage:str, targetLanguage:str):
        """
        text: 需要翻译的文本
        appid: 百度翻译API的appid
        secretKey: 百度翻译API的密钥
        originalLanguage: 原文语言
        targetLanguage: 译文语言
        return：翻译结果
        """
        salt = random.randint(32768, 65536)
        sign = hashlib.md5((str(appid)+text+str(salt)+secretKey).encode()).hexdigest()
        targetURL = "http://api.fanyi.baidu.com/api/trans/vip/translate"+"?appid="+str(appid)+"&q="+urllib.parse.quote(text)+"&from="+originalLanguage+"&to="+targetLanguage+"&salt="+str(salt)+"&sign="+sign
        httpClient = None
        # 建立会话，返回结果
        try:
            httpClient = http.client.HTTPConnection("api.fanyi.baidu.com")
            httpClient.request("GET", targetURL)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            trans_result = result["trans_result"][0]["dst"]
        except Exception as err:
            logger.critical(repr(err))
            msgbox.showerror(message=f"服务器发生错误，无法进行翻译，请到此日的log中查看详细报错信息（在“/logs/{datetime.date.today()}.log”）。", title="翻译器")
        finally:
            if httpClient:
                httpClient.close()
                return trans_result
        return None
    def JSONtoXML(json_file_path:str, xml_file_path:str):
        """
        json_file_path: JSON文件路径
        xml_file_path: 保存的XML文件路径
        return :
            0 => 成功
            1 => JSON文件不存在
            2 => JSON文件读取失败
        """
        try :
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)
                xml_data = str(dicttoxml.dicttoxml(json_data))
                with open(xml_file_path, "w", encoding="utf-8") as xml_file:
                    xml_file.write(xml_data)
                    return 0
        except FileNotFoundError:
            logger.error("JSON file not found: {}".format(json_file_path))
            msgbox.showerror(message="JSON文件不存在！", title="JSON to XML")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="JSON文件读取失败！", title="JSON to XML")
            return 2
    def XMLtoJSON(xml_file_path:str, json_file_path:str):
        """
        xml_file_path: XML文件路径
        json_file_path: 保存的JSON文件路径
        return :
            0 => 成功
            1 => XML文件不存在
            2 => XML文件读取失败
        """
        try :
            with open(xml_file_path, "r", encoding="utf-8") as xml_file:
                xml_data = xml_file.read()
                json_data = json.dumps(xmltodict.parse(xml_data), ensure_ascii=False)
                with open(json_file_path, "w", encoding="utf-8") as json_file:
                    json_file.write(json_data)
                    return 0
        except FileNotFoundError:
            logger.error("XML file not found: {}".format(xml_file_path))
            msgbox.showerror(message="XML文件不存在！", title="XML to JSON")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="XML文件读取失败！", title="XML to JSON")
            return 2
    def getIP(domain=socket.gethostname()):
        """
        domain: 域名
        return :
            IP地址
        """
        try :
            return socket.gethostbyname(domain)
        except socket.error as err:
            return repr(err)
    def resolveDomain(ip):
        """
        ip: IP地址
        return :
            域名
        """
        try:
            domain = socket.gethostbyaddr(ip)
            return domain[0]
        except socket.error as err:
            return repr(err)
    class FileDiffTools():
        def __init__(self):
            text1 = self.readFromFile(askopenfilename(title="选择文件1", filetypes=(("纯文本文件", "*.txt"), ("所有文件", "*.*"))))
            text2 = self.readFromFile(askopenfilename(title="选择文件2", filetypes=(("纯文本文件", "*.txt"), ("所有文件", "*.*"))))
            result = self.diffTexts(text1, text2, asksaveasfilename(title="保存文件", filetypes=(("HTML文件", "*.html"), ("所有文件", "*.*"))))
            logger.info("Save file successfully!")
            if result == 0:
                msgbox.showinfo(title="提示", message="保存文件成功！")
            else:
                msgbox.showerror(title="错误", message="保存文件失败！\n退出代码: {}".format(result))
        def readFromFile(self, fpath):
            """
            从文件读取文本
            fpath: 文件路径
            return: 文本内容
            """
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read().splitlines()
        def diffTexts(self, text1:str, text2:str, fpath:str):
            """
            对比两段文本并且将结果保存到HTML文件中
            text1: 文本1
            text2: 文本2
            fpath: 保存的HTML文件路径
            return: 错误码
                0: 成功
                1: 参数有问题
                2: 文件读取失败
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
        msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
        logger.error("Invocation error")
    def charPicture(filename):
        """
        filename: 图片文件名
        """
        color = "MNHQ$OC?7>!:-;."  # 字符
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
            # 定义 HTML
            def wrapper(img):
                pic_str = func(img)
                pic_str = "".join(l + " <br/>" for l in pic_str.splitlines())
                return html_head + pic_str + html_tail
            return wrapper
        # 绘制字符画
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
        logger.info(f"Output file:{filename}-char.html")
        msgbox.showinfo(title="输出成功", message="文件已经输出在和图片同一级目录下！")
    def bingPicture(fname:str, idx:str="0", mkt:str="zh-cn"):
        """
        获取Bing每日一图
        fname: 保存的文件名称
        idx: 时间：
            0: 今天
            -1: 明天（预准备的）
            1: 昨天
            2: 前天
            3~7 类推
        mkt: 地区，使用微软地区码，例如：zh-cn: 中国大陆、en-us: 美国
        return: 退出码
        """
        try:
            NUMBER = 1
            IDX = idx
            MKT = mkt
            FORMAT = "js"
            USER_AGENT = {
                'Content-Type':'application/json; charset=utf-8',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            }
            requestURL = "https://cn.bing.com/HPImageArchive.aspx?" + f"format={FORMAT}&idx={IDX}&n={NUMBER}&mkt={MKT}"
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
        msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
        logger.error("Invocation error")
    class DevToolsLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
            logger.error("Invocation error")
        def webConnectTestLauncher():
            try :
                with open("logs/records.log", "r") as r:
                    try :
                        record = r.readlines()[len(r.readlines()) - 1]
                    except IndexError:
                        record = ""
            except FileNotFoundError:
                record = ""
            url = easygui.enterbox(msg="输入URL（带“http://”）", title="Windows 实用工具", default=record)
            logger.info(f"User input: {url}")
            if (url != None):
                record = url
                if not(settings["no-log-file"]):
                    with open("logs/records.log", "a") as record_log:
                        record_log.write(f"\n{record}")
            if (url != None):
                global DevTools
                result = DevTools.webConnectTest(url)
                msgbox.showinfo(title="Windows 实用工具",message=result)
                if not("协议不存在，您是否忘记在网站开头加上“http://”？" in result):
                    logger.info(f"Web address connect info: {url} => {result}")
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
                result = msgbox.askokcancel(message="百度翻译需要您的AppID和秘钥才能使用。是否输入？\n翻译器承诺绝对不会把您的隐私泄露。", title="翻译器", icon="warning")
                if result == True:
                    datas = easygui.multpasswordbox("输入AppID和秘钥。", title="翻译器", fields=["AppID", "秘钥"])
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
                text = easygui.enterbox("输入文本", title="翻译器")
                if text:
                    fromLang = "auto"
                    toLang = easygui.choicebox("想输出的语言？", choices=list(languages.keys()), title="翻译器")
                    logger.info(f"User input:[{text}, {fromLang}, {languages[toLang]}]")
                    if (text != None)and(fromLang != None)and(toLang != None):
                        result = DevTools.translator(text, id, key, fromLang, languages[toLang])
                        msgbox.showinfo(message=f"翻译完成！\n原文：{text}\n翻译后：{result}\n翻译语言：{toLang}\n（如果结果内有“None”您却没有输入“None”，大概是翻译失败）", title="翻译器")
                        logger.info(f"Result: {result}")
                    else :
                        msgbox.showerror(message="缺少参数！", title="翻译器")
                        logger.error("Missing arguments")
        def JSONtoXMLLauncher():
            json = easygui.fileopenbox(title="打开文件", filetypes=[["*.json", "JSON files"]], default="*.json")
            xml = easygui.filesavebox(title="保存文件", filetypes=[["*.xml", "XML files"]], default="*.xml")
            if (json != None):
                if (os.path.splitext(json)[-1] == ".json"):
                    global DevTools
                    logger.info(f"Input JSON:{json}")
                    DevTools.JSONtoXML(json, xml)
                    logger.info(f"Output finish")
                else :
                    msgbox.showerror(title="错误", message="文件拓展名不是\".json\"！")
                    logger.error("File extension is incorrect")
        def XMLtoJSONLauncher():
            xml = easygui.fileopenbox(title="打开文件", filetypes=[["*.xml", "XML files"]], default="*.xml")
            json = easygui.filesavebox(title="保存文件", filetypes=[["*.json", "JSON files"]], default="*.json")
            if (xml != None):
                if (os.path.splitext(xml)[-1] == ".xml"):
                    global DevTools
                    logger.info(f"Input XML:{xml}")
                    DevTools.XMLtoJSON(xml, json)
                    logger.info(f"Output finish")
                else :
                    msgbox.showerror(title="错误", message="文件拓展名不是\".xml\"！")
                    logger.error("File extension is incorrect")
        def getIPLauncher():
            ip = easygui.enterbox("输入域名\n或者输入“@default”使用本地域名", title="IP地址获取器")
            if (ip != None):
                if (ip != "@default"):
                    global DevTools
                    logger.info(f"Input IP:{ip}")
                    result = DevTools.getIP(ip)
                    msgbox.showinfo(message=f"IP地址：{result}", title="IP地址获取器")
                    logger.info(f"Result: {result}")
                else :
                    logger.info(f"Input IP:{ip}")
                    result = DevTools.getIP()
                    msgbox.showinfo(message=f"IP地址：{result}", title="IP地址获取器")
                    logger.info(f"Result: {result}")
        def resolveDomainLauncher():
            domain = easygui.enterbox("输入IP地址", title="域名解析器")
            if (domain != None):
                global DevTools
                logger.info(f"Input Domain: {domain}")
                result = DevTools.resolveDomain(domain)
                msgbox.showinfo(message=f"解析结果：{result}", title="域名解析器")
                logger.info(f"Result: {result}")
    class DrawingToolsLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
            logger.error("Invocation error")
        def charPictureLauncher():
            path = easygui.fileopenbox(title="打开文件", filetypes=[["*.jpg", "*.jpeg" , "JPG files"], ["*.bmp", "BMP files"], ["*.gif", "GIF files"]], default="*.png")
            if (path != None):
                if (os.path.splitext(path)[-1] == ".png")or(os.path.splitext(path)[-1] == ".jpg")or(os.path.splitext(path)[-1] == ".bmp")or(os.path.splitext(path)[-1] == ".gif")or(os.path.splitext(path)[-1] == ".jpeg"):
                    global DrawingTools
                    logger.info(f"Input picture:{path}")
                    DrawingTools.charPicture(path)
                else :
                    msgbox.showerror(title="错误", message="文件拓展名错误！")
                    logger.error("File extension is incorrect")
        def bingPictureLauncher():
            fname = asksaveasfilename(title="保存文件", filetypes=[["JPG Files", "*.jpg"]], defaultextension="*.jpg")
            if (fname != None):
                logger.info(f"Input path: {fname}")
                if (os.path.splitext(fname)[-1] == ".jpg"):
                    params = easygui.multenterbox(title="必应每日一图", msg="请输入信息。", fields=["索引", "地区码"])
                    if (params != None != ["","",""]):
                        if (params[0].isdigit())or(params[0] == "-1"):
                            params.insert(0, fname)
                            logger.info(f"Input params:{params}")
                            global DrawingTools
                            DrawingTools.bingPicture(params[0], params[1], params[2])
                            logger.info("Done.")
                            msgbox.showinfo(title="提示", message="图片已保存至指定路径。")
                        else :
                            msgbox.showerror(title="错误", message="索引必须为数字！")
                            return
                else :
                    logger.error("File extension is incorrect")
                    msgbox.showerror(title="错误", message="文件拓展名错误！")
                    return
    class ExternalLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
            logger.error("Invocation error")
        def webSpeedTsetLauncher():
            def run():
                subprocess.Popen("python /src/webspeedtest/main.py")
            msgbox.showwarning(title="警告", message="本程序等待时间极长，大约2分钟，将在后台进行测速操作。\n等待期间仍可以正常使用此程序。")
            thread = threading.Thread(target=run)
            thread.start()
        def clockLauncher():
            subprocess.Popen("python src/clock/main.py") # python src/clock/main.py
        def calculatorLauncher():
            subprocess.Popen("calc")
        def hashCheckerLauncher():
            msgbox.showinfo(title="Windows 实用工具", message="HASH校验器在src/tools/hash.py，请根据提示使用")
        def passwordCreatorLauncher():
            subprocess.Popen("python src/passwordCreator/main.py") # python "src\passwordCreator\main.py"
        def licenceCreatorLauncher():
            subprocess.Popen("python src/licenceCreator/main.py")
        def qrcodeGeneratorLauncher():
            subprocess.Popen("python src/qrcode/main.py 0")
        def qrcodeParserLauncher():
            subprocess.Popen("python src/qrcode/main.py 1")

class System():
    def about():
        msgbox.showinfo(title="Windows 实用工具", message="""Windows 实用工具 v2.1.5 zh-cn
作者：@wangzixin1940
编辑器：JetBrains Pycharm 和 Microsoft Visual Studio Code
当前运行的Python文件：main.py
发行日期：2024-5-19
自述文件：README.md (en-US and zh-CN)
MIT License：https://github.com/wangzixin1940/Windows-Utilities/blob/main/LICENCE
VERSION 2.1 RELEASE
""")
    def languageSettings():
        msgbox.showerror(title="Windows Utilities", message="Please run \"release/en-US/main.py\" to run the English version of this program")
    def quitApp():
        root.destroy()
    def switchTheme():
        if msgbox.askokcancel(title="Windows 实用工具", message="是否切换主题？\n切换后需要重新启动程序才能生效。打开后本程序会自动关闭。", icon="warning"):
            subprocess.Popen("python tools/configurator.py") # python "tools\configurator.py"
            root.destroy()
    def importSettings():
        path = easygui.fileopenbox(title="打开文件", filetypes=[["*.json", "JSON files"]], default="*.json")
        global settings
        if (path != None):
            if (msgbox.askokcancel(title="Windows 实用工具", message="是否导入设置？\n现有的配置文件将会被覆盖。\n损坏的配置文件可能会导致程序运行错误。", icon="warning")):
                with open(path, "r+", encoding="utf-8") as new_settings:
                    new_settings = new_settings.read()
                    new_settings = json.loads(new_settings)
                    logger.info(f"Settings: {new_settings}")
                    with open("data/settings.json", "w+", encoding="utf-8") as settings:
                        settings.write(json.dumps(new_settings, ensure_ascii=False, indent=4))
                        msgbox.showinfo(title="Windows 实用工具", message="设置已导入。")
                        logger.info("Settings imported")

def main():
    global root
    global style
    root = ttk.Window()
    with open("./data/theme.json", "r", encoding="utf-8") as theme:
        theme = theme.read()
        theme = json.loads(theme)
    logger.info("Starting APP")
    root.title("Windows 实用工具")
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
            logger.warning("Icon file not found. Program will use default icon and cosmo theme.")
    style.configure("TButton", font=("等线 Light", 18, "normal"), width=20, height=3)
    style.configure("TMenubutton", font=("等线 Light", 18, "normal"), width=19, height=3)
    # 窗口
    # ===================================== #
    title = ttk.Label(root, text="Windows 实用工具", font=("等线 Light",22,"normal"))
    title.pack() # 工具的标题
    # ===================================== #
    utilitiesLabel = ttk.Label(root, text="实用工具 🛠", font=("等线 Light",18,"normal"))
    utilitiesLabel.pack() # 实用工具标签
    translateButton = ttk.Button(root, text="翻译器", command=Launcher.DevToolsLauncher.translatorLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    translateButton.pack() # 翻译器按钮
    # ===================================== #
    DevToolsLabel = ttk.Label(root, text="开发者工具 </>", font=("等线 Light",18,"normal"))
    DevToolsLabel.pack() # 开发者工具标签
    connectButton = ttk.Button(root, text="检测网站状态码", command=Launcher.DevToolsLauncher.webConnectTestLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    connectButton.pack() # 检测网络连接
    speedTestButton = ttk.Button(root, text="测网速",command=Launcher.ExternalLauncher.webSpeedTsetLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speedTestButton.pack() # 测速按钮
    # ===================================== #
    externalsLabel = ttk.Label(root, text="其他工具 🧰", font=("等线 Light",18,"normal"))
    externalsLabel.pack() # 其他工具标签
    passwordCreatorButton = ttk.Button(root, text="密码生成器", command=Launcher.ExternalLauncher.passwordCreatorLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    passwordCreatorButton.pack() # 密码生成器按钮
    # ===================================== #
    if not(settings["no-menu"]):
        menu = ttk.Menu(root)
        fileMenu = ttk.Menu(menu)
        otherMenu = ttk.Menu(menu)
        settingsMenu = ttk.Menu(menu)
        menu.add_cascade(label="文件", menu=fileMenu)
        menu.add_cascade(label="其他", menu=otherMenu)
        if not(settings["no-settings-menu"]):
            menu.add_cascade(label="设置", menu=settingsMenu)
        menu.add_command(label="关于", command=System.about)
        fileMenu.add_command(label="导入设置", command=System.importSettings)
        fileMenu.add_command(label="退出", command=System.quitApp)
        otherMenu.add_command(label="计算器", command=Launcher.ExternalLauncher.calculatorLauncher)
        otherMenu.add_command(label="校验md5", command=Launcher.ExternalLauncher.hashCheckerLauncher)
        otherMenu.add_command(label="Licence 创造器", command=Launcher.ExternalLauncher.licenceCreatorLauncher)
        ipToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="IP工具", menu=ipToolsMenu)
        ipToolsMenu.add_command(label="IP地址查询", command=Launcher.DevToolsLauncher.getIPLauncher)
        ipToolsMenu.add_command(label="解析IP地址", command=Launcher.DevToolsLauncher.resolveDomainLauncher)
        fileToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="文件工具", menu=fileToolsMenu)
        fileToolsMenu.add_command(label="JSON转XML", command=Launcher.DevToolsLauncher.JSONtoXMLLauncher)
        fileToolsMenu.add_command(label="XML转JSON", command=Launcher.DevToolsLauncher.XMLtoJSONLauncher)
        fileToolsMenu.add_command(label="文件对比", command=DevTools.FileDiffTools)
        qrcodeToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="二维码工具", menu=qrcodeToolsMenu)
        qrcodeToolsMenu.add_command(label="生成二维码", command=Launcher.ExternalLauncher.qrcodeGeneratorLauncher)
        qrcodeToolsMenu.add_command(label="解析二维码", command=Launcher.ExternalLauncher.qrcodeParserLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(label="字符画", command=Launcher.DrawingToolsLauncher.charPictureLauncher)
        otherMenu.add_command(label="Bing每日一图", command=Launcher.DrawingToolsLauncher.bingPictureLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(label="时钟", command=Launcher.ExternalLauncher.clockLauncher)
        if not(settings["no-settings-menu"]):
            settingsMenu.add_command(label="颜色主题", command=System.switchTheme)
            settingsMenu.add_command(label="语言设置", command=System.languageSettings)
        root.config(menu=menu)
    # 工具栏
    # ===================================== #
    root.mainloop()


if __name__ == '__main__':
    logger.info("Platform: {system} {version}".format(system=sysinfo["system"], version=sysinfo["version"]))
    logger.info("Python: {version} {implementation}".format(version=sysinfo["python"]["version"], implementation=sysinfo["python"]["implementation"]))
    # 输出系统信息
    if sysinfo["python"]["version"][0] >= 3:
        if sysinfo["python"]["version"][1] >= 8:
            main(); exit(0)
        else:
            logger.warning("Python Version too old: {}".format(sysinfo["python"]["version"]))
    else:
        logger.warning("Python Version too old: {}".format(sysinfo["python"]["version"]))
    main(); exit(1)

