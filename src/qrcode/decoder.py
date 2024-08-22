from PIL import Image
import pyzbar.pyzbar as pyzbar

import json
import logging
import datetime

import io
import sys
import os

os.chdir(os.path.dirname(__file__))
# Replace the working directory

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the console output


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
        # Configure the logger
        self.logger.info("The configuration is done.")

    def decodeQRcode(self, image: str):
        """
        QR code decoding
        Args:
            image: QR code image path
        Returns:
            QR code content
        """
        result = pyzbar.decode(
            Image.open(image), symbols=[
                pyzbar.ZBarSymbol.QRCODE])  # Parsing QR codes
        """                          ↑↑↑
        The above code comes from: https://blog.csdn.net/smallfox233/article/details/119408399
        """
        self.logger.info(f"Decode was sucessful.")
        return result[0].data.decode("utf-8")
