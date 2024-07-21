"""
Special note:
The data for this program comes from WWIS (World Weather Information Service, https://worldweather.wmo.int/).
"""

import datetime
import logging
import json
import requests
from tkinter import messagebox as msgbox
import ttkbootstrap as ttk
import csv
import os
os.chdir(os.path.dirname(__file__))
# Change working directory to the directory of this file


logging.basicConfig(
    filename=f"../../logs/{datetime.date.today()}.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("WEATHER_APP")
# Set up logger


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Weather Queries")
        self.geometry("400x300")
        self.resizable(False, False)
        self.iconbitmap("assets/favicon.ico")
        self.styleset = ttk.Style()
        self.styleset.theme_use("cosmo")
        self.styleset.configure("TButton", font=("Airal", 12), width=15)
        # Create widgets
        self.maintitle = ttk.Label(
            self, text="Weather Queries", font=(
                "Airal", 20))
        self.country = ttk.Label(
            self, text="Name of Country:", font=(
                "Airal", 12))
        self.entry = ttk.Entry(self, width=40)
        self.city = ttk.Label(self, text="Name of City:", font=("Airal", 12))
        self.entry2 = ttk.Entry(self, width=40)
        self.search = ttk.Button(
            self, text="INQUIRE", command=self.search_weather)
        # Layout widgets
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
        Search for weather
        """
        id = self.search_id()
        if id == -1:
            msgbox.showerror(
                "Error",
                "This city is not included. Please check the input.\nOr check data/full_city_list.csv to find your city ID (Third column).")
            return
        try:
            content = requests.get(
                f"https://worldweather.wmo.int/en/json/{id}_en.json")
            json_data = content.content.decode("utf-8")
            data = json.loads(json_data)
            logger.info(data)
            text = f"""Query successful!
{self.entry2.get()}'s weather：
Forecast for tomorrow: {data["city"]["forecast"]["forecastDay"][0]["weather"]}
Forecast for day after tomorrow: {data["city"]["forecast"]["forecastDay"][1]["weather"]}
Forecast for {data["city"]["forecast"]["forecastDay"][2]["forecastDate"]}: {data["city"]["forecast"]["forecastDay"][2]["weather"]}
Forecast for {data["city"]["forecast"]["forecastDay"][3]["forecastDate"]}: {data["city"]["forecast"]["forecastDay"][3]["weather"]}
Forecast for {data["city"]["forecast"]["forecastDay"][4]["forecastDate"]}: {data["city"]["forecast"]["forecastDay"][4]["weather"]}
Forecast for {data["city"]["forecast"]["forecastDay"][5]["forecastDate"]}: {data["city"]["forecast"]["forecastDay"][5]["weather"]}
"""
            msgbox.showinfo("Query successful", text)
        except requests.exceptions.ConnectionError as err:
            msgbox.showerror(
                "Error",
                "Network connection error, please check your network connection.")
            logger.error(repr(err))
            return
        except Exception as err:
            msgbox.showerror("Error", "Unknown error.")
            logger.error(repr(err))
            return


if __name__ == "__main__":
    try:
        with open("data/full_city_list.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            city_list = list(reader)
    except FileNotFoundError:
        msgbox.showerror(
            "Error",
            "The city list file was not found. Please check the file path.")
        exit(1)
    except OSError:
        msgbox.showerror(
            "Error",
            "An error occurred while reading the city list file")
        exit(2)
    App()
