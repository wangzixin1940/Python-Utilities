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
# Change the default encoding to UTF-8

os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script

warnings.warn("This feature has been deprecated because the speedtest library has been discontinued for maintenance.", DeprecationWarning)

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings.json file

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
    # Download speed
    download_speed = int(tester.download() / 1024 / 1024)
    # Upload speed
    upload_speed = int(tester.upload() / 1024 / 1024)
    logger.info(
        f"Download Speed:{download_speed} MB; Upload Speed:{upload_speed} MB")
    return (download_speed, upload_speed)

# print(webSpeedTest())


root = tkinter.Window()
root.title("Web Speed Test")
root.geometry("350x350")
root.resizable(False, False)

txt = scrolledtext.ScrolledText(root, width=45, height=20)
txt.grid(column=0, row=0)

txt.pack()

txt.insert(
    tkinter.INSERT,
    "Internet Speed Test Program (Standalone)\nBased-on SpeedTest.net's SpeedTest Module\nVersion 1.1 en-US\n")
result = webSpeedTest()
txt.insert(tkinter.INSERT,
           f"Upload：{result[1]} MBits/s; Download：{result[0]} MBits/s")
txt.config(state=tkinter.DISABLED)

root.mainloop()
