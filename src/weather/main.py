"""
Special Instructions:
The data for this program are from WWIS (World Weather Information Service, https://worldweather.wmo.int/).
"""

import datetime
import logging
import requests
from tkinter import messagebox as msgbox
import ttkbootstrap as ttk
import csv

import os
import json

os.chdir(os.path.dirname(__file__))
# Change the working directory to the current file's directory

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["weather"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]

logging.basicConfig(
    filename=f"../../logs/{datetime.date.today()}.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("WEATHER_APP")
# Configure the logger


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title(ui["title"])
        self.geometry("400x300")
        self.resizable(False, False)
        self.iconbitmap("assets/favicon.ico")
        self.styleset = ttk.Style()
        self.styleset.theme_use("cosmo")
        self.styleset.configure("TButton", font=("Airal", 12), width=15)
        # Create widgets
        self.maintitle = ttk.Label(self, text=ui["title"], font=("Airal", 20))
        self.country = ttk.Label(self, text=ui["country"], font=("Airal", 12))
        self.entry = ttk.Entry(self, width=40)
        self.city = ttk.Label(self, text=ui["city"], font=("Airal", 12))
        self.entry2 = ttk.Entry(self, width=40)
        self.search = ttk.Button(self, text=ui["search"], command=self.search_weather)
        # Pack widgets
        self.maintitle.pack(pady=10)
        self.country.pack(anchor="w")
        self.entry.pack(anchor="w")
        self.city.pack(anchor="w")
        self.entry2.pack(anchor="w")
        self.search.pack(pady=10)
        # Main loop
        self.mainloop()

    def search_id(self) -> int:
        """
        Find the city ID
        Returns:
            City ID
        """
        country = self.entry.get()
        city = self.entry2.get()
        for i in city_list:
            if country == i[0] and city == i[1]:
                if not (i[2].isdigit()):
                    return i[3]
                return i[2]
        return -1

    def search_weather(self):
        """
        Check the weather and display it
        Returns:
            None (if error occurred)
        """
        id = self.search_id()
        if id == -1:
            msgbox.showerror(
                ui_src["error"], ui["infos"]["notIncludedError"])
            return
        try:
            content = requests.get(
                f"https://worldweather.wmo.int/en/json/{id}_en.json")
            json_data = content.content.decode("utf-8")
            data = json.loads(json_data)
            logger.info(data)
            text = f"""
{ui["infos"]["weather"]}
{ui["infos"]["forecast_for_tomorrow"]}
{ui["infos"]["forecast_for_day_after_tomorrow"]}
{ui["infos"]["forecastForDay4"]}
{ui["infos"]["forecastForDay5"]}
{ui["infos"]["forecastForDay6"]}
{ui["infos"]["forecastForDay7"]}
"""
            text = text.format(
                city=self.entry2.get(),
                tomorrow=data["city"]["forecast"]["forecastDay"][0]["weather"],
                dat=data["city"]["forecast"]["forecastDay"][1]["weather"],
                day4=data["city"]["forecast"]["forecastDay"][2]["forecastDate"],
                day4f=data["city"]["forecast"]["forecastDay"][2]["weather"],
                day5=data["city"]["forecast"]["forecastDay"][3]["forecastDate"],
                day5f=data["city"]["forecast"]["forecastDay"][3]["weather"],
                day6=data["city"]["forecast"]["forecastDay"][4]["forecastDate"],
                day6f=data["city"]["forecast"]["forecastDay"][4]["weather"],
                day7=data["city"]["forecast"]["forecastDay"][5]["forecastDate"],
                day7f=data["city"]["forecast"]["forecastDay"][5]["weather"]
            )
            msgbox.showinfo(ui["infos"]["complete"], text)
        except requests.exceptions.ConnectionError as err:
            msgbox.showerror(ui_src["error"], ui["infos"]["errorNetwork"])
            logger.error(repr(err))
            return
        except Exception as err:
            msgbox.showerror(ui_src["error"], ui["infos"]["unknownError"])
            logger.error(repr(err))
            return


if __name__ == "__main__":
    try:
        with open("data/full_city_list.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            city_list = list(reader)
    except FileNotFoundError:
        msgbox.showerror(ui_src["error"], ui["infos"]["errorDataNotFound"])
        exit(1)
    except OSError:
        msgbox.showerror(ui_src["error"], ui["infos"]["errorData"])
        exit(2)
    App()
