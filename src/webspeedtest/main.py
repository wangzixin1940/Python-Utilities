from tkinter import scrolledtext
import ttkbootstrap as tkinter
import datetime
import logging
import speedtest
import io
import sys
import warnings


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
# Change sys.stdout encoding to utf-8

import os
import json

os.chdir(os.path.dirname(__file__))
# Change working directory to the directory of the script

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["speedtest"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]

warnings.warn("This feature has been deprecated because the speedtest library has been discontinued for maintenance.", DeprecationWarning)

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
root.title(ui["title"])
root.geometry("350x350")
root.resizable(False, False)

txt = scrolledtext.ScrolledText(root, width=45, height=20)
txt.grid(column=0, row=0)

txt.pack()  # The title of the text box

txt.insert(
    tkinter.INSERT,
    ui["about"])
result = webSpeedTest()
txt.insert(tkinter.INSERT, ui["info"].format(up=result[0], down=result[1]))
txt.config(state=tkinter.DISABLED)

root.mainloop()
