import qrcode
from qrcode.image.styledpil import StyledPilImage

import json
import logging
import datetime

import io
import sys
import os

os.chdir(os.path.dirname(__file__))
# Change the working directory to the current file's directory

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the standard output to the encoding specified in the settings file


class Encoder():
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
        # Configure log information
        self.logger.info("The configuration is done.")

    def generateQRcode(
            self,
            data: str,
            filename: str,
            module_drawer=None,
            color_mask=None,
            embeded_image_path: str | None = None,
            *args):
        """
        Generate a QR code
        Args:
            data: QR code data
            filename: Save the file name of the QR code
            module_drawer: Drawer
            color_mask: Color mask
            embeded_image_path: Embeded image path
        """
        qr = qrcode.main.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
        )
        qr.add_data(data)
        qr.make(data)
        if embeded_image_path and module_drawer and color_mask:
            img = qr.make_image(
                *args,
                image_factory=StyledPilImage,
                module_drawer=module_drawer,
                color_mask=color_mask,
                embeded_image=embeded_image_path)
        elif embeded_image_path and module_drawer:
            img = qr.make_image(
                *args,
                image_factory=StyledPilImage,
                module_drawer=module_drawer,
                embeded_image=embeded_image_path)
        elif embeded_image_path and color_mask:
            img = qr.make_image(
                *args,
                image_factory=StyledPilImage,
                color_mask=color_mask,
                embeded_image=embeded_image_path)
        elif module_drawer and color_mask:
            img = qr.make_image(
                *args,
                image_factory=StyledPilImage,
                module_drawer=module_drawer,
                color_mask=color_mask)
        elif module_drawer:
            img = qr.make_image(
                *args,
                image_factory=StyledPilImage,
                module_drawer=module_drawer)
        elif color_mask:
            img = qr.make_image(
                *args,
                image_factory=StyledPilImage,
                color_mask=color_mask)
        elif embeded_image_path:
            img = qr.make_image(
                *args,
                image_factory=StyledPilImage,
                embeded_image=embeded_image_path)
        else:
            img = qr.make_image(*args, image_factory=StyledPilImage, )
        self.logger.info("Generating done.")
        if (filename.endswith(".png")):
            img.save(filename)
        else:
            self.logger.warning("The file format is not supported.")
            img.save(filename)
        self.logger.info("Saving done.")
