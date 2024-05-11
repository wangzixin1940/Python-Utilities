import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
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

# 工具所需模块
import requests
from PIL import Image
import os
import http.client
import hashlib
import urllib
import random
import json
import subprocess
import threading


logging.basicConfig(
                filename=f"./logs/{datetime.date.today()}.log",
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ROOT")
# print(logger.__dict__)
# 配置日志信息



class DevTools():
    def __init__(self):
        msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
        logger.error("INVOCATION ERROR")
    def webConnectTest(url:str):
        """
        测试网站是否可以访问
        url: 网站URL
        """
        try :
            result = str(requests.get(url).status_code)
        except requests.exceptions.MissingSchema as err:
            logger.critical("MISSING SCHEMA ERROR")
            return f"协议不存在，您是否忘记在网站开头加上“http://”？\n{err}"
        # 返回HTTP状态码
        # print(result)
        with open("./data/connect.test.codes.json", "r") as statusCodes:
            statusCodes = statusCodes.read()
            statusCodes = json.loads(statusCodes)
        # 常见的HTTP状态码列表
        try :
            return str(result) + "：" + statusCodes[result]
        except KeyError:
            logger.error(f"STATUS CODE:{result} NOT FOUND")
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
        # print(targetURL)
        httpClient = None
        # 建立会话，返回结果
        try:
            httpClient = http.client.HTTPConnection("api.fanyi.baidu.com")
            httpClient.request("GET", targetURL)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            # print(result, flush=True)
            trans_result = result["trans_result"][0]["dst"]
            # print(trans_result, flush=True)
        except Exception as err:
            logger.critical(err)
            msgbox.showerror(message=f"服务器发生错误，无法进行翻译，请到此日的log中查看详细报错信息（在“/logs/{datetime.date.today()}.log”）。", title="翻译器")
        finally:
            if httpClient:
                httpClient.close()
                return trans_result
        return None

class DrawingTools():
    def __init__(self):
        msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
        logger.error("INVOCATION ERROR")
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
                logger.debug("FILE WAS SUCCESSFULLY SAVED")
                outfile.write(pic_str)
        img = preprocess(filename)
        pic_str = make_char_img(img)
        save_to_file(f"{filename}-char.html", pic_str)
        logger.info(f"OUTPUT FILE:{filename}-char.html")
        msgbox.showinfo(title="输出成功", message="文件已经输出在和图片同一级目录下！")
class Launcher():
    def __init__(self):
        msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
        logger.error("INVOCATION ERROR")
    class DevToolsLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
            logger.error("INVOCATION ERROR")
        def webConnectTestLauncher():
            with open("logs/records.log", "r") as r:
                try :
                    record = r.readlines()[len(r.readlines()) - 1]
                except IndexError:
                    record = ""
            url = easygui.enterbox(msg="输入URL（带“http://”）", title="Windows 实用工具", default=record)
            logger.info(f"USER INPUT:{url}")
            if (url != None):
                record = url
                with open("logs/records.log", "a") as record_log:
                    record_log.write(f"\n{record}")
            if (url != None):
                global DevTools
                result = DevTools.webConnectTest(url)
                msgbox.showinfo(title="Windows 实用工具",message=result)
                if not("协议不存在，您是否忘记在网站开头加上“http://”？" in result):
                    logger.info(f"WEB ADDRESS CONNECT INFO: {url} => {result}")
        def translatorLauncher():
            try:
                with open("data/translator.appid.json", "r") as appid:
                    appid = appid.read()
                    appid = json.loads(appid)
                    id = appid["id"]
                    key = appid["key"]
                entered = True
            except (FileNotFoundError, KeyError) as err:
                logger.error(err)
                result = msgbox.askokcancel(message="百度翻译需要您的AppID和秘钥才能使用。是否输入？\n翻译器承诺绝对不会把您的隐私泄露。", title="翻译器", icon="warning")
                if result == True:
                    datas = easygui.multpasswordbox("输入AppID和秘钥。", title="翻译器", fields=["AppID", "秘钥"])
                    id = datas[0]
                    key = datas[1]
                    entered = True
                    with open("data/translator.appid.json", "w") as appid:
                        appid.write(json.dumps({"id":id, "key":key}))
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
                    # print(languages.keys())
                    logger.info(f"USER INPUT:[{text}, {fromLang}, {languages[toLang]}]")
                    if (text != None)and(fromLang != None)and(toLang != None):
                        result = DevTools.translator(text, id, key, fromLang, languages[toLang])
                        msgbox.showinfo(message=f"翻译完成！\n原文：{text}\n翻译后：{result}\n翻译语言：{toLang}\n（如果结果内有“None”您却没有输入“None”，大概是翻译失败）", title="翻译器")
                        logger.info(f"RESULT:{result}")
                    else :
                        msgbox.showerror(message="缺少参数！", title="翻译器")
                        logger.error("MISSING ARGUMENTS")
    class DrawingToolsLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
            logger.error("INVOCATION ERROR")
        def charPictureLauncher():
            path = easygui.fileopenbox(title="打开文件", filetypes=[["*.jpg", "*.jpeg" , "JPG files"], ["*.bmp", "BMP files"], ["*.gif", "GIF files"]], default="*.png")
            if (path != None):
                if (os.path.splitext(path)[-1] == ".png")or(os.path.splitext(path)[-1] == ".jpg")or(os.path.splitext(path)[-1] == ".bmp")or(os.path.splitext(path)[-1] == ".gif")or(os.path.splitext(path)[-1] == ".jpeg"):
                    global DrawingTools
                    logger.info(f"INPUT PICTURE:{path}")
                    DrawingTools.charPicture(path)
                else :
                    msgbox.showerror(title="错误", message="文件拓展名错误！")
                    logger.error("FILE EXTENSION IS INCORRECT")
    class ExternalLauncher():
        def __init__(self):
            msgbox.showerror(title="错误", message="调用错误！请调用此类的子项。")
            logger.error("INVOCATION ERROR")
        def webSpeedTsetLauncher():
            def run():
                subprocess.Popen("python ./src/webspeedtest/main.py")
            msgbox.showwarning(title="警告", message="本程序等待时间极长，大约2分钟，将在后台进行测速操作。\n等待期间仍可以正常使用此程序。")
            thread = threading.Thread(target=run)
            thread.start()
        def clockLauncher():
            subprocess.Popen("python \"src\\clock\\main.py\"") # python "src\clock\main.py"
        def calculatorLauncher():
            subprocess.Popen("calc")
        def md5CheckerLauncher():
            msgbox.showinfo(title="Windows 实用工具", message="MD5校验器在\"src\\cmdtools\\md5.py\"，请根据提示使用")
        def passwordCreatorLauncher():
            subprocess.Popen("python \"src\\passwordCreator\\main.py\"") # python "src\passwordCreator\main.py"

class System():
    def about():
        msgbox.showinfo(title="Windows 实用工具", message="""Windows 实用工具 v1.10.1 zh-cn
作者：@wangzixin1940
编辑器：JetBrains Pycharm 和 Microsoft Visual Studio Code
当前运行的Python文件：/main.py
发行日期：2024-4-6
VERSION 1.9 RELEASE
""")
    def languageSettings():
        msgbox.showerror(title="Windows 实用工具", message="EN-US版本未推出，等待您的翻译！\nThe EN-US version is not yet available. Waiting for your translation!")
    def quitApp():
        root.destroy()
    def switchTheme():
        if msgbox.askokcancel(title="Windows 实用工具", message="是否切换主题？\n切换后需要重新启动程序才能生效。打开后本程序会自动关闭。", icon="warning"):
            subprocess.Popen("python \"tools\\configurator.py\"") # python "tools\configurator.py"
            root.destroy()

def main():
    global root
    global style
    root = ttk.Window()
    with open("./data/theme.json", "r", encoding="utf-8") as settings:
        settings = settings.read()
        settings = json.loads(settings)
    logger.info("STARTING APP")
    root.title("Windows 实用工具")
    root.geometry("500x550")
    root.resizable(False, False)
    if settings["theme"] == "pride":
        root.iconbitmap("./images/pride.ico")
        style = ttk.Style("cosmo")
    else :
        root.iconbitmap("./images/icon.ico")
        style = ttk.Style(settings["theme"])
    style.configure("TButton", font=("等线 Light",18,"normal"), width=20, height=3)
    # 窗口
    # ===================================== #
    title = ttk.Label(root, text="Windows 实用工具", font=("等线 Light",22,"normal"))
    title.pack() # 工具的标题
    # ===================================== #
    DevToolsLabel = ttk.Label(root, text="开发者工具🛠️", font=("等线 Light",18,"normal"))
    DevToolsLabel.pack() # 开发者工具标签
    connectButton = ttk.Button(root, text="检测网站状态码", command=Launcher.DevToolsLauncher.webConnectTestLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    connectButton.pack() # 检测网络连接
    translateButton = ttk.Button(root, text="翻译器", command=Launcher.DevToolsLauncher.translatorLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    translateButton.pack() # 翻译器按钮
    speedTestButton = ttk.Button(root, text="测网速",command=Launcher.ExternalLauncher.webSpeedTsetLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speedTestButton.pack() # 测速按钮
    # ===================================== #
    DrawingToolsLabel = ttk.Label(root, text="绘画工具🎨", font=("等线 Light",18,"normal"))
    DrawingToolsLabel.pack() # 绘画工具标签
    charPictureButton = ttk.Button(root, text="字符画", command=Launcher.DrawingToolsLauncher.charPictureLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    charPictureButton.pack() # 字符画按钮
    # ===================================== #
    externalsLabel = ttk.Label(root, text="其他工具 🧰", font=("等线 Light",18,"normal"))
    externalsLabel.pack() # 其他工具标签
    passwordCreatorButton = ttk.Button(root, text="密码生成器", command=Launcher.ExternalLauncher.passwordCreatorLauncher, bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    passwordCreatorButton.pack() # 密码生成器按钮
    # ===================================== #
    menu = ttk.Menu(root)
    fileMenu = ttk.Menu(menu)
    otherMenu = ttk.Menu(menu)
    settingsMenu = ttk.Menu(menu)
    menu.add_cascade(label="文件", menu=fileMenu)
    menu.add_cascade(label="其他", menu=otherMenu)
    menu.add_cascade(label="设置", menu=settingsMenu)
    menu.add_command(label="关于", command=System.about)
    fileMenu.add_command(label="语言设置", command=System.languageSettings)
    fileMenu.add_command(label="退出", command=System.quitApp)
    otherMenu.add_command(label="计算器", command=Launcher.ExternalLauncher.calculatorLauncher)
    otherMenu.add_command(label="校验md5", command=Launcher.ExternalLauncher.md5CheckerLauncher)
    otherMenu.add_command(label="时钟", command=Launcher.ExternalLauncher.clockLauncher)
    settingsMenu.add_command(label="颜色主题", command=System.switchTheme)
    root.config(menu=menu)
    # 工具栏
    # ===================================== #
    root.mainloop()


if __name__ == '__main__':
    main()

