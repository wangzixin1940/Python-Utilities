from PIL import Image
import pyzbar.pyzbar as pyzbar

import json
import logging
import datetime

import io
import sys
import os

os.chdir(os.path.dirname(__file__))
# 更换工作目录

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # 读取设置文件

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# 更换编码


class Decoder():
    def __init__(self):
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
        self.logger = logging.getLogger("QRCODE-DECODER")
        # 配置日志信息
        self.logger.info("The configuration is done.")

    def decodeQRcode(self, image: str):
        """
        二维码解码
        image: 二维码图片路径
        return: 二维码内容
        """
        result = pyzbar.decode(
            Image.open(image), symbols=[
                pyzbar.ZBarSymbol.QRCODE])  # 解析二维码
        """                          ↑↑↑
        以上代码来自：https://blog.csdn.net/smallfox233/article/details/119408399
        """
        self.logger.info(f"Decode was sucessful.")
        return result[0].data.decode("utf-8")
