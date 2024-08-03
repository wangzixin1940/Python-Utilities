import json
from tkinter import scrolledtext
import ttkbootstrap as tkinter
import datetime
import logging
import speedtest
import os
import io
import sys
import warnings


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
# 更换编码

os.chdir(os.path.dirname(__file__))
# 更换工作目录

warnings.warn("This feature has been deprecated because the speedtest library has been discontinued for maintenance.", DeprecationWarning)

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # 读取设置文件

if not (settings["no-log-file"]):
    logging.basicConfig(
        filename=f"../../logs/{datetime.date.today()}.log",
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
logger = logging.getLogger("SPEEDTEST")


def webSpeedTest():
    logger.info("Prepare for the test")
    tester = speedtest.Speedtest()
    tester.get_servers()
    # theBest = tester.get_best_server()
    logger.info("Start testing")
    # 下载速度
    download_speed = int(tester.download() / 1024 / 1024)
    # 上传速度
    upload_speed = int(tester.upload() / 1024 / 1024)
    logger.info(
        f"Download Speed:{download_speed} MB; Upload Speed:{upload_speed} MB")
    return (download_speed, upload_speed)

# print(webSpeedTest())


root = tkinter.Window()
root.title("网速测试小程序")
root.geometry("350x350")
root.resizable(False, False)

txt = scrolledtext.ScrolledText(root, width=45, height=20)
txt.grid(column=0, row=0)

txt.pack()  # 文本框的标题

txt.insert(
    tkinter.INSERT,
    "网速测试程序（独立版）\n基于SpeedTest.net的SpeedTest库构建\n版本 1.1\n")
result = webSpeedTest()
txt.insert(tkinter.INSERT, f"上传：{result[0]} MBits/s; 下载：{result[1]} MBits/s")
txt.config(state=tkinter.DISABLED)

root.mainloop()
