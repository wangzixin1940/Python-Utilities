"""
特别说明：
本程序的数据均来自WWIS(World Weather Information Service，https://worldweather.wmo.int/)。
"""

import os
os.chdir(os.path.dirname(__file__))
# 更换工作目录

import logging, datetime

logging.basicConfig(
                    filename=f"../../logs/{datetime.date.today()}.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("WEATHER_APP")

import csv
import ttkbootstrap as ttk
from tkinter import messagebox as msgbox
import requests
import json
import time

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("天气查询")
        self.geometry("400x300")
        self.resizable(False, False)
        self.iconbitmap("assets/favicon.ico")
        self.styleset = ttk.Style()
        self.styleset.theme_use("cosmo")
        self.styleset.configure("TButton", font=("微软雅黑", 12), width=15)
        # 创建控件
        self.maintitle = ttk.Label(self, text="天气查询", font=("微软雅黑", 20))
        self.country = ttk.Label(self, text="请输入国家名称：", font=("微软雅黑", 12))
        self.entry = ttk.Entry(self, width=40)
        self.city = ttk.Label(self, text="请输入城市名称：", font=("微软雅黑", 12))
        self.entry2 = ttk.Entry(self, width=40)
        self.search = ttk.Button(self, text="查询", command=self.search_weather)
        # 布局控件
        self.maintitle.pack(pady=10)
        self.country.pack(anchor="w")
        self.entry.pack(anchor="w")
        self.city.pack(anchor="w")
        self.entry2.pack(anchor="w")
        self.search.pack(pady=10)
        # 主循环
        self.mainloop()

    def search_id(self) -> int:
        """
        查找城市ID
        """
        country = self.entry.get()
        city = self.entry2.get()
        for i in city_list:
            if country == i[0] and city == i[1]:
                if not(i[2].isdigit()):
                    return i[3]
                return i[2]
        return -1
        
    def search_weather(self):
        """
        查询天气并且显示
        """
        id = self.search_id()
        if id == -1:
            msgbox.showerror("错误", "未收录此城市，请检查输入。\n或者查看data/full_city_list.csv文件查找您的城市ID（第三列）。")
            return
        try:
            content = requests.get(f"https://worldweather.wmo.int/en/json/{id}_en.json")
            json_data = content.content.decode("utf-8")
            data = json.loads(json_data)
            logger.info(data)
            text = f"""查询成功！
{self.entry2.get()}的天气：
今天：{data["city"]["forecast"]["forecastDay"][0]["weather"]}
明天预测：{data["city"]["forecast"]["forecastDay"][1]["weather"]}
后天预测：{data["city"]["forecast"]["forecastDay"][2]["weather"]}
{data["city"]["forecast"]["forecastDay"][3]["forecastDate"]}预测：{data["city"]["forecast"]["forecastDay"][3]["weather"]}
{data["city"]["forecast"]["forecastDay"][4]["forecastDate"]}预测：{data["city"]["forecast"]["forecastDay"][4]["weather"]}
{data["city"]["forecast"]["forecastDay"][5]["forecastDate"]}预测：{data["city"]["forecast"]["forecastDay"][5]["weather"]}
"""
            msgbox.showinfo("查询成功", text)
        except requests.exceptions.ConnectionError as err:
            msgbox.showerror("错误", "网络连接错误，请检查网络连接。")
            logger.error(repr(err))
            return
        except Exception as err:
            msgbox.showerror("错误", "未知错误。")
            logger.error(repr(err))
            return



if __name__ == "__main__":
    try:
        with open("data/full_city_list.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            city_list = list(reader)
    except FileNotFoundError:
        msgbox.showerror("错误", "未找到城市列表文件，请检查文件路径。")
        exit(1)
    except OSError:
        msgbox.showerror("错误", "读取城市列表文件时发生错误。")
        exit(2)
    App()
