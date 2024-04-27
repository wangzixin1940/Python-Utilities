import speedtest
import logging
import datetime
import ttkbootstrap as tkinter
from tkinter import scrolledtext

logging.basicConfig(
                filename=f"./logs/{datetime.date.today()}.log",
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("USER-COMMAND")

def webSpeedTest():
        logger.info("PREPARE FOR THE TEST")
        tester = speedtest.Speedtest()
        tester.get_servers()
        # theBest = tester.get_best_server()
        logger.info("START TESTING")
        # 下载速度
        download_speed = int(tester.download() / 1024 / 1024)
        # 上传速度
        upload_speed = int(tester.upload() / 1024 / 1024)
        logger.info(f"DS:{download_speed} MB; US:{upload_speed} MB")
        return (download_speed, upload_speed)

# print(webSpeedTest())

root = tkinter.Window()
root.title("网速测试小程序")
root.geometry("350x350")
root.resizable(False, False)

txt = scrolledtext.ScrolledText(root, width=45, height=20)
txt.grid(column=0, row=0)

txt.pack() # 文本框的标题

txt.insert(tkinter.INSERT, "网速测试程序（独立版）\n基于SpeedTest.net的SpeedTest库构建\n版本 1.1\n")
result = webSpeedTest()
txt.insert(tkinter.INSERT, f"上传：{result[0]} MBits/s；下载：{result[1]} MBits/s")
txt.config(state = tkinter.DISABLED)

root.mainloop()