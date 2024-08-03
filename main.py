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
    # 读取设置文件

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# 更换编码


os.chdir(os.path.dirname(__file__))
# 更换工作目录


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
# 配置日志信息

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
        msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
        logger.error("Invocation error")

    def webConnectTest(url: str):
        """
        测试网站是否可以访问
        url: 网站URL
        """
        try:
            result = str(requests.get(url).status_code)
        except requests.exceptions.MissingSchema as err:
            logger.critical("Missing schema error")
            return f"协议不存在，您是否忘记在网站开头加上“https://”？\n{repr(err)}"
        # 返回HTTP状态码
        with open("./data/connect.test.codes.json", "r") as status_codes:
            status_codes = status_codes.read()
            status_codes = json.loads(status_codes)
        # 常见的HTTP状态码列表
        try:
            return str(result) + "：" + status_codes[result]
        except KeyError:
            logger.error(f"Status code: {result} not found")
            return f"网站返回了一个未知的HTTP状态码：{result}"
        # 如果HTTP状态码已知，则返回结果；否则提示用户返回未知状态码

    def translator(text: str, appid: str, secret_key: str, original_language: str, target_language: str):
        """
        text: 需要翻译的文本
        appid: 百度翻译API的appid
        secret_key: 百度翻译API的密钥
        original_language: 原文语言
        target_language: 译文语言
        return：翻译结果
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
        # 建立会话，返回结果
        try:
            http_client = http.client.HTTPConnection("api.fanyi.baidu.com")
            http_client.request("GET", target_url)
            # response是HTTPResponse对象
            response = http_client.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            trans_result = result["trans_result"][0]["dst"]
        except Exception as err:
            logger.critical(repr(err))
            msgbox.showerror(
                message=f"服务器发生错误，无法进行翻译，请到此日的log中查看详细报错信息（在“/logs/{datetime.date.today()}.log”）。",
                title="翻译器")
        finally:
            if http_client:
                http_client.close()
                if trans_result:
                    return trans_result
        return None

    def JSONtoXML(json_file_path: str, xml_file_path: str):
        """
        json_file_path: JSON文件路径
        xml_file_path: 保存的XML文件路径
        return :
            0 => 成功
            1 => JSON文件不存在
            2 => JSON文件读取失败
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
            msgbox.showerror(message="JSON文件不存在！", title="JSON to XML")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="JSON文件读取失败！", title="JSON to XML")
            return 2

    def XMLtoJSON(xml_file_path: str, json_file_path: str):
        """
        xml_file_path: XML文件路径
        json_file_path: 保存的JSON文件路径
        return :
            0 => 成功
            1 => XML文件不存在
            2 => XML文件读取失败
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
            msgbox.showerror(message="XML文件不存在！", title="XML to JSON")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="XML文件读取失败！", title="XML to JSON")
            return 2

    def CSVtoJSON(csv_file_path: str, json_file_path: str):
        """
        csv_file_path: CSV文件路径
        json_file_path: 保存的JSON文件路径
        return :
            0 => 成功
            1 => CSV文件不存在
            2 => CSV文件读取失败
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
            logger.error("CSV file not found: {}".format(csv_file_path))
            msgbox.showerror(message="CSV文件不存在！", title="CSV to JSON")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="CSV文件读取失败！", title="CSV to JSON")
            return 2

    def JSONtoCSV(json_file_path: str, csv_file_path: str):
        """
        json_file_path: JSON文件路径
        csv_file_path: CSV文件路径
        return :
            0 => 成功
            1 => JSON文件不存在
            2 => JSON文件读取失败
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
            msgbox.showerror(message="JSON文件不存在！", title="JSON to CSV")
            return 1
        except Exception as err:
            logger.error(repr(err))
            msgbox.showerror(message="JSON文件读取失败！", title="JSON to CSV")
            return 2

    def getIP(domain=socket.gethostname()):
        """
        domain: 域名
        return :
            IP地址
        """
        try:
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
            text1 = self.readFromFile(
                fdg.askopenfilename(title="选择文件1", filetypes=(("纯文本文件", "*.txt"), ("所有文件", "*.*"))))
            text2 = self.readFromFile(
                fdg.askopenfilename(title="选择文件2", filetypes=(("纯文本文件", "*.txt"), ("所有文件", "*.*"))))
            result = self.diffTexts(text1, text2, fdg.asksaveasfilename(title="保存文件", filetypes=(
                ("HTML文件", "*.html"), ("所有文件", "*.*"))))
            logger.info("Save file successfully!")
            if result == 0:
                msgbox.showinfo(title="提示", message="保存文件成功！")
            else:
                msgbox.showerror(
                    title="错误", message="保存文件失败！\n退出代码: {}".format(result))

        @staticmethod
        def readFromFile(fpath):
            """
            从文件读取文本
            fpath: 文件路径
            return: 文本内容
            """
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read().splitlines()

        @staticmethod
        def diffTexts(text1: str, text2: str, fpath: str):
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
                                body {
                                    font-family: Monospace;
                                    font-size: 5px;
                                }
                            </style>
                        </head>
                    <body> '''
            html_tail = "</body> </html>"

            # 定义 HTML
            def wrapper(image):
                pic_string = func(image)
                pic_string = "".join(line + " <br />" for line in pic_string.splitlines())
                return html_head + pic_string + html_tail

            return wrapper

        # 绘制字符画
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
        msgbox.showinfo(title="输出成功", message="文件已经输出在和图片同一级目录下！")

    def bingPicture(fname: str, idx: str = "0", mkt: str = "zh-cn"):
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
        msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
        logger.error("Invocation error")

    class DevToolsLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
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
                msg="输入URL（带“https://”）", title="Python Utilities", default=record)
            logger.info(f"User input: {url}")
            if (url != None):
                record = url
                if not (settings["no-log-file"]):
                    with open("logs/records.log", "a") as record_log:
                        record_log.write(f"\n{record}")
            if (url != None):
                global DevTools
                result = DevTools.webConnectTest(url)
                msgbox.showinfo(title="Python Utilities", message=result)
                if not ("协议不存在，您是否忘记在网站开头加上“https://”？" in result):
                    logger.info(f"Web address connect info: {url} => {result}")

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
                    message="百度翻译需要您的AppID和秘钥才能使用。是否输入？\n翻译器承诺绝对不会把您的隐私泄露。",
                    title="翻译器", icon="warning")
                if result:
                    datas = easygui.multpasswordbox(
                        "输入AppID和秘钥。", title="翻译器", fields=["AppID", "秘钥"])
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
                text = easygui.enterbox("输入文本", title="翻译器")
                if text:
                    fromLang = "auto"
                    toLang = easygui.choicebox(
                        "想输出的语言？", choices=list(languages.keys()), title="翻译器")
                    logger.info(
                        f"User input:[{text}, {fromLang}, {languages[toLang]}]")
                    if (text != None) and (fromLang != None) and (toLang != None):
                        result = DevTools.translator(
                            text, id, key, fromLang, languages[toLang])
                        msgbox.showinfo(
                            message=f"翻译完成！\n原文：{text}\n翻译后：{result}\n翻译语言：{toLang}\n（如果结果内有“None”您却没有输入“None”，大概是翻译失败）",
                            title="翻译器")
                        logger.info(f"Result: {result}")
                    else:
                        msgbox.showerror(message="缺少参数！", title="翻译器")
                        logger.error("Missing arguments")

        @staticmethod
        def JSONtoXMLLauncher():
            json = easygui.fileopenbox(title="打开文件", filetypes=[
                                       ["*.json", "JSON files"]], default="*.json")
            xml = easygui.filesavebox(title="保存文件", filetypes=[
                                      ["*.xml", "XML files"]], default="*.xml")
            if (json != None):
                if (os.path.splitext(json)[-1] == ".json"):
                    global DevTools
                    logger.info(f"Input JSON:{json}")
                    DevTools.JSONtoXML(json, xml)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(title="错误", message="文件拓展名不是\".json\"！")
                    logger.error("File extension is incorrect")

        @staticmethod
        def XMLtoJSONLauncher():
            xml = easygui.fileopenbox(title="打开文件", filetypes=[
                                      ["*.xml", "XML files"]], default="*.xml")
            json = easygui.filesavebox(title="保存文件", filetypes=[
                                       ["*.json", "JSON files"]], default="*.json")
            if (xml != None):
                if (os.path.splitext(xml)[-1] == ".xml"):
                    global DevTools
                    logger.info(f"Input XML:{xml}")
                    DevTools.XMLtoJSON(xml, json)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(title="错误", message="文件拓展名不是\".xml\"！")
                    logger.error("File extension is incorrect")

        @staticmethod
        def getIPLauncher():
            global DevTools
            ip = easygui.enterbox(
                "输入域名\n或者输入“@default”使用本地域名", title="IP地址获取器")
            if (ip != None):
                if (ip != "@default"):
                    global DevTools
                    logger.info(f"Input IP:{ip}")
                    result = DevTools.getIP(ip)
                    msgbox.showinfo(message=f"IP地址：{result}", title="IP地址获取器")
                    logger.info(f"Result: {result}")
                else:
                    logger.info(f"Input IP:{ip}")
                    result = DevTools.getIP()
                    msgbox.showinfo(message=f"IP地址：{result}", title="IP地址获取器")
                    logger.info(f"Result: {result}")

        @staticmethod
        def resolveDomainLauncher():
            domain = easygui.enterbox("输入IP地址", title="域名解析器")
            if (domain != None):
                global DevTools
                logger.info(f"Input Domain: {domain}")
                result = DevTools.resolveDomain(domain)
                msgbox.showinfo(message=f"解析结果：{result}", title="域名解析器")
                logger.info(f"Result: {result}")

        @staticmethod
        def JSONtoCSVLauncher():
            json = easygui.fileopenbox(title="打开文件", filetypes=[
                                       ["*.json", "JSON files"]], default="*.json")
            csv = easygui.filesavebox(title="保存文件", filetypes=[
                                      ["*.csv", "CSV files"]], default="*.csv")
            if (json != None):
                if (os.path.splitext(json)[-1] == ".json"):
                    global DevTools
                    logger.info(f"Input JSON:{json}")
                    DevTools.JSONtoCSV(json, csv)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(title="错误", message="文件拓展名不是\".json\"！")
                    logger.error("File extension is incorrect")

        @staticmethod
        def CSVtoJSONLauncher():
            csv = easygui.fileopenbox(title="打开文件", filetypes=[
                                      ["*.csv", "CSV files"]], default="*.csv")
            json = easygui.filesavebox(title="保存文件", filetypes=[
                                       ["*.json", "JSON files"]], default="*.json")
            if (csv != None):
                if (os.path.splitext(csv)[-1] == ".csv"):
                    global DevTools
                    logger.info(f"Input CSV:{csv}")
                    DevTools.CSVtoJSON(csv, json)
                    logger.info(f"Output finish")
                else:
                    msgbox.showerror(title="错误", message="文件拓展名不是\".csv\"！")
                    logger.error("File extension is incorrect")

    class DrawingToolsLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
            logger.error("Invocation error")

        @staticmethod
        def charPictureLauncher():
            path = easygui.fileopenbox(title="打开文件",
                                       filetypes=[["*.jpg", "*.jpeg", "JPG files"], ["*.bmp", "BMP files"],
                                                  ["*.gif", "GIF files"]], default="*.png")
            if (path != None):
                if (os.path.splitext(path)[-1] == ".png") or (os.path.splitext(path)[-1] == ".jpg") or (
                        os.path.splitext(path)[-1] == ".bmp") or (os.path.splitext(path)[-1] == ".gif") or (
                        os.path.splitext(path)[-1] == ".jpeg"):
                    global DrawingTools
                    logger.info(f"Input picture:{path}")
                    DrawingTools.charPicture(path)
                else:
                    msgbox.showerror(title="错误", message="文件拓展名错误！")
                    logger.error("File extension is incorrect")

        @staticmethod
        def bingPictureLauncher():
            fname = fdg.asksaveasfilename(title="保存文件", filetypes=[["JPG Files", "*.jpg"]],
                                          defaultextension="*.jpg")
            if (fname != None):
                logger.info(f"Input path: {fname}")
                if (os.path.splitext(fname)[-1] == ".jpg"):
                    params = easygui.multenterbox(
                        title="必应每日一图", msg="请输入信息。", fields=["索引", "地区码"])
                    if (params != None != ["", "", ""]):
                        if (params[0].isdigit()) or (params[0] == "-1"):
                            params.insert(0, fname)
                            logger.info(f"Input params:{params}")
                            global DrawingTools
                            DrawingTools.bingPicture(
                                params[0], params[1], params[2])
                            logger.info("Done.")
                            msgbox.showinfo(title="提示", message="图片已保存至指定路径。")
                        else:
                            msgbox.showerror(title="错误", message="索引必须为数字！")
                            return
                else:
                    logger.error("File extension is incorrect")
                    msgbox.showerror(title="错误", message="文件拓展名错误！")
                    return

    class ExternalLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
            logger.error("Invocation error")

        @staticmethod
        def webSpeedTsetLauncher():
            def run():
                subprocess.Popen("python /src/webspeedtest/main.py")

            msgbox.showwarning(title="警告",
                               message="本程序等待时间极长，大约2分钟，将在后台进行测速操作。\n等待期间仍可以正常使用此程序。")
            thread = threading.Thread(target=run)
            thread.start()

        @staticmethod
        def clockLauncher():
            # python src/clock/main.py
            subprocess.Popen("python src/clock/main.py")

        @staticmethod
        def calculatorLauncher():
            subprocess.Popen("python src/calculator/main.py")

        @staticmethod
        def hashCheckerLauncher():
            msgbox.showinfo(title="Python Utilities",
                            message="HASH校验器在src/tools/hash.py，请根据提示使用")

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


class System():
    @staticmethod
    def about():
        msgbox.showinfo(title="Python Utilities", message="""Python Utilities v2.8.0 BETA zh-cn
作者：@wangzixin1940
编辑器：JetBrains Pycharm 和 Microsoft Visual Studio Code
当前运行的Python文件：main.py
发行日期：2024-7-3
自述文件：README.md (en-US and zh-CN)
GNU GPLv3 License：https://github.com/wangzixin1940/Windows-Utilities/blob/main/LICENCE
VERSION 2.8 (BETA) RELEASE
""")

    @staticmethod
    def languageSettings():
        subprocess.Popen("python release/en-US/main.py")
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
        path = easygui.fileopenbox(title="打开文件", filetypes=[
                                   ["*.json", "JSON files"]], default="*.json")
        global settings
        if (path != None):
            if (msgbox.askokcancel(title="Python Utilities",
                                   message="是否导入设置？\n现有的配置文件将会被覆盖。\n损坏的配置文件可能会导致程序运行错误。",
                                   icon="warning")):
                with open(path, "r+", encoding="utf-8") as new_settings:
                    new_settings = new_settings.read()
                    new_settings = json.loads(new_settings)
                    logger.info(f"Settings: {new_settings}")
                    with open("data/settings.json", "w+", encoding="utf-8") as settings:
                        settings.write(json.dumps(
                            new_settings, ensure_ascii=False, indent=4))
                        msgbox.showinfo(
                            title="Python Utilities", message="设置已导入。")
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
        "等线 Light", 18, "normal"), width=20, height=3)
    style.configure("TMenubutton", font=(
        "等线 Light", 18, "normal"), width=19, height=3)
    # 窗口
    # ===================================== #
    title = ttk.Label(root, text="Python Utilities",
                      font=("等线 Light", 22, "normal"))
    title.pack()  # 工具的标题
    # ===================================== #
    utilitiesLabel = ttk.Label(
        root, text="实用工具 🛠", font=("等线 Light", 18, "normal"))
    utilitiesLabel.pack()  # 实用工具标签
    translateButton = ttk.Button(text="翻译器", command=Launcher.DevToolsLauncher.translatorLauncher,
                                 bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    translateButton.pack()  # 翻译器按钮
    weatherButton = ttk.Button(root, text="天气预报", command=Launcher.ExternalLauncher.weatherLauncher,
                               bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    weatherButton.pack()  # 天气预报按钮
    speech2textButton = ttk.Button(root, text="语音转文字", command=Launcher.ExternalLauncher.speech2textLauncher,
                                   bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speech2textButton.pack()  # 语音转文字按钮
    # ===================================== #
    DevToolsLabel = ttk.Label(root, text="开发者工具 </>",
                              font=("等线 Light", 18, "normal"))
    DevToolsLabel.pack()  # 开发者工具标签
    connectButton = ttk.Button(text="检测网站状态码", command=Launcher.DevToolsLauncher.webConnectTestLauncher,
                               bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    connectButton.pack()  # 检测网络连接
    speedTestButton = ttk.Button(root, text="测网速", command=Launcher.ExternalLauncher.webSpeedTsetLauncher,
                                 bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speedTestButton.pack()  # 测速按钮
    # ===================================== #
    externalsLabel = ttk.Label(
        root, text="其他工具 🧰", font=("等线 Light", 18, "normal"))
    externalsLabel.pack()  # 其他工具标签
    passwordCreatorButton = ttk.Button(root, text="密码生成器",
                                       command=Launcher.ExternalLauncher.passwordCreatorLauncher,
                                       bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    passwordCreatorButton.pack()  # 密码生成器按钮
    # ===================================== #
    if not (settings["no-menu"]):
        menu = ttk.Menu(root)
        fileMenu = ttk.Menu(menu)
        otherMenu = ttk.Menu(menu)
        settingsMenu = ttk.Menu(menu)
        menu.add_cascade(label="文件", menu=fileMenu)
        menu.add_cascade(label="其他", menu=otherMenu)
        if not (settings["no-settings-menu"]):
            menu.add_cascade(label="设置", menu=settingsMenu)
        menu.add_command(label="关于", command=System.about)
        fileMenu.add_command(label="导入设置", command=System.importSettings)
        fileMenu.add_command(label="退出", command=System.quitApp)
        otherMenu.add_command(
            label="计算器", command=Launcher.ExternalLauncher.calculatorLauncher)
        otherMenu.add_command(
            label="校验md5", command=Launcher.ExternalLauncher.hashCheckerLauncher)
        otherMenu.add_command(
            label="Licence 创造器", command=Launcher.ExternalLauncher.licenceCreatorLauncher)
        otherMenu.add_command(
            label="用JSON批量发送邮件", command=Launcher.ExternalLauncher.sendMailFromJSONLauncher)
        ipToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="IP工具", menu=ipToolsMenu)
        ipToolsMenu.add_command(
            command=Launcher.DevToolsLauncher.getIPLauncher)
        ipToolsMenu.add_command(
            command=Launcher.DevToolsLauncher.resolveDomainLauncher)
        fileToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="文件工具", menu=fileToolsMenu)
        fileToolsMenu.add_command(
            command=Launcher.DevToolsLauncher.JSONtoXMLLauncher)
        fileToolsMenu.add_command(
            command=Launcher.DevToolsLauncher.XMLtoJSONLauncher)
        fileToolsMenu.add_command(
            label="JSON转CSV", command=Launcher.DevToolsLauncher.JSONtoCSVLauncher)
        fileToolsMenu.add_command(
            label="CSV转JSON", command=Launcher.DevToolsLauncher.CSVtoJSONLauncher)
        fileToolsMenu.add_command(label="文件对比", command=DevTools.FileDiffTools)
        qrcodeToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label="二维码工具", menu=qrcodeToolsMenu)
        qrcodeToolsMenu.add_command(
            label="生成二维码", command=Launcher.ExternalLauncher.qrcodeGeneratorLauncher)
        qrcodeToolsMenu.add_command(
            label="解析二维码", command=Launcher.ExternalLauncher.qrcodeParserLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(
            label="字符画", command=Launcher.DrawingToolsLauncher.charPictureLauncher)
        otherMenu.add_command(
            label="Bing每日一图", command=Launcher.DrawingToolsLauncher.bingPictureLauncher)
        otherMenu.add_command(
            label="照片格式转换", command=Launcher.ExternalLauncher.pictureFormatConverterLauncher)
        otherMenu.add_command(
            label="脚本操作鼠标和键盘", command=Launcher.ExternalLauncher.AMKLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(
            label="时钟", command=Launcher.ExternalLauncher.clockLauncher)
        if not (settings["no-settings-menu"]):
            themesMenu = ttk.Menu(settingsMenu)
            settingsMenu.add_cascade(label="颜色主题", menu=themesMenu)
            for i in style.theme_names():
                themesMenu.add_radiobutton(
                    label=i, command=lambda name=i: System.switchTheme(name)
                )
            themesMenu.add_separator()
            themesMenu.add_command(
                label="pride", command=lambda: System.switchTheme("pride"))
            settingsMenu.add_command(
                label="Switch to English...", command=System.languageSettings)
        root.config(menu=menu)
    # 工具栏
    # ===================================== #
    root.mainloop()


if __name__ == '__main__':
    logger.info("Platform: {system} {version}".format(
        system=sysinfo["system"], version=sysinfo["version"]))
    logger.info("Python: {version} {implementation}".format(version=sysinfo["python"]["version"],
                                                            implementation=sysinfo["python"]["implementation"]))
    # 输出系统信息
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
