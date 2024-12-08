import json
import logging, datetime
import requests


with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the standard output

with open(settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)  # type: dict[str: dict]

logging.basicConfig(
        filename=f"./logs/{datetime.date.today()}.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ARTTOOLS")


from PIL import Image
from PySide6.QtWidgets import QMessageBox, QApplication

app = QApplication([])


def charPicture(filename):
    """
    Convert pictures to ascii art
    Args:
        filename: The file name of the image
    """
    color = "MNHQ$OC?7>!:-;."  # characters
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
        # HTML definition
        def wrapper(image):
            pic_string = func(image)
            pic_string = "".join(line + " <br />" for line in pic_string.splitlines())
            return html_head + pic_string + html_tail
        return wrapper

    # Draw ascii art
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
    QMessageBox.information(None, ui["asciiArt"]["successTitle"], ui["asciiArt"]["successMessage"])

def bingPicture(filename: str, idx: str = "0", mkt: str = "zh-cn"):
    """
    Get Bing's Daily Graph
    Args:
        filename: The name of the saved file
        idx: Time index
            0: Today
            -1: Tomorrow (pre-prepared)
            1: Yesterday
            2: Day before yesterday
            3~7 analogy
        mkt: Region, using Microsoft region codes, e.g. zh-cn: Chinese mainland, en-us: United States
    Returns:
        Exit code
    """
    try:
        NUMBER = 1
        IDX = idx
        MKT = mkt
        FORMAT = "js"
        USER_AGENT = {
            'Content-Type': 'application/json; charset=utf-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36',
        }
        requestURL = "https://www.bing.com/HPImageArchive.aspx?" + \
                     f"format={FORMAT}&idx={IDX}&n={NUMBER}&mkt={MKT}"
        response = requests.get(requestURL, headers=USER_AGENT)
        if response.status_code == 200:
            try:
                if NUMBER == 1:
                    data = response.json()
                    data = "https://www.bing.com" + data["images"][0]["url"]
                    with open(filename, 'wb') as f:
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
