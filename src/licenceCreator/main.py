from tkinter import messagebox as msgbox
from tkinter.filedialog import asksaveasfile
import ttkbootstrap as ttk
import os
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# 更换编码

os.chdir(os.path.dirname(__file__))
# 更换工作目录

import json

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["licenceCreator"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]

with open("models/apache-v2.txt", "r", encoding="utf-8") as apache:
    apache_licence = apache.read()

with open("models/mit.txt", "r", encoding="utf-8") as mit:
    mit_licence = mit.read()

with open("models/gpl-v3.txt", "r", encoding="utf-8") as gpl:
    gpl_licence = gpl.read()

with open("models/isc.txt", "r", encoding="utf-8") as isc:
    isc_licence = isc.read()
# 导入LICENCE模版


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title(ui["title"])
        self.geometry("600x600")
        self.resizable(False, False)
        style = self.style
        style.theme_use("cosmo")
        self.iconbitmap("assets/icon.ico")
        # 创建界面
        self.mainlabel = ttk.Label(
            self, text=ui["title"], font=(
                "Arial", 18))
        self.mainlabel.grid(row=0, column=0, pady=10, padx=10, rowspan=2)
        # 创建主标题
        self.licence_label = ttk.Label(
            self, text=ui["typeChoose"], font=(
                "Arial", 15))
        self.licence_label.grid(row=2, column=0, pady=10, padx=10)
        # 创建下拉菜单
        self.licence_var = ttk.StringVar(self)
        self.licences = ttk.Menu(self)
        self.licence_menu = ttk.Menubutton(
            self, textvariable=self.licence_var, width=10, menu=self.licences)
        self.licences.add_command(
            label="Apache 2.0",
            command=lambda: self.licence_var.set("apache"))
        self.licences.add_command(label="MIT",
                                  command=lambda: self.licence_var.set("mit"))
        self.licences.add_command(label="GPL 3.0",
                                  command=lambda: self.licence_var.set("gpl"))
        self.licences.add_command(label="ISC",
                                  command=lambda: self.licence_var.set("isc"))
        self.licence_menu.grid(row=2, column=1, pady=10, padx=10)
        # 创建子标题
        self.params_label = ttk.Label(
            self, text=ui["params"]["label"], font=(
                "Arial", 15, "bold"))
        self.params_label.grid(row=3, column=0, pady=10, padx=10)
        # 创建参数输入框
        self.name_label = ttk.Label(self, text=ui["params"]["name"], font=("Arial", 12))
        self.name_label.grid(row=4, column=0, pady=10, padx=10)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=4, column=1, pady=10, padx=10)
        self.year_label = ttk.Label(self, text=ui["params"]["year"], font=("Arial", 12))
        self.year_label.grid(row=5, column=0, pady=10, padx=10)
        self.year_entry = ttk.Spinbox(self, width=18)
        self.year_entry.grid(row=5, column=1, pady=10, padx=10)
        self.usage_label = ttk.Label(self, text=ui["params"]["usage"], font=("Arial", 12))
        self.usage_label.grid(row=6, column=0, pady=10, padx=10)
        self.usage_entry = ttk.Entry(self)
        self.usage_entry.grid(row=6, column=1, pady=10, padx=10)
        self.project_name_label = ttk.Label(
            self, text=ui["params"]["projectName"], font=("Arial", 12))
        self.project_name_label.grid(row=7, column=0, pady=10, padx=10)
        self.project_name_entry = ttk.Entry(self)
        self.project_name_entry.grid(row=7, column=1, pady=10, padx=10)
        # 创建按钮
        self.create_button = ttk.Button(
            self, text=ui["create"], command=self.create_licence)
        self.create_button.grid(
            row=8,
            column=0,
            pady=10,
            padx=10,
            rowspan=2,
            sticky="nsew")

    def create_licence(self):
        # 获取参数
        name = self.name_entry.get()
        year = self.year_entry.get()
        usage = self.usage_entry.get()
        project_name = self.project_name_entry.get()
        # 创建LicenceCreator对象
        licenceCreator = LicenceCreator(
            self.licence_var.get(), {
                "name": name, "year": year, "usage": usage, "project_name": project_name})
        # 保存Licence
        path = asksaveasfile(
            defaultextension="LICENCE.txt", filetypes=[
                file_types["txt"], file_types["no"]])
        if path:
            path.write(licenceCreator.licence)
            path.close()
            msgbox.showinfo(ui["complete"], ui["saveComplete"])


class LicenceCreator():
    def __init__(self, licence: str, params: dict):
        self.licence = licence
        if licence == "apache":
            self.make_apache_licence(params["name"], params["year"])
        elif licence == "mit":
            self.make_mit_licence(params["name"], params["year"])
        elif licence == "gpl":
            self.make_gpl_licence(
                params["name"],
                params["year"],
                params["usage"],
                params["project_name"])
        elif licence == "isc":
            self.make_isc_licence(params["name"], params["year"])
        else:
            raise self.LicenceNotFound("Licence not found: {}".format(licence))

    def make_apache_licence(self, name: str, year: int):
        self.name = name
        self.year = year
        self.licence = apache_licence.format(str(year), name)

    def make_mit_licence(self, name: str, year: int):
        self.name = name
        self.year = year
        self.licence = mit_licence.format(str(year), name)

    def make_gpl_licence(
            self,
            name: str,
            year: int,
            usage: str,
            project_name: str):
        self.name = name
        self.year = year
        self.usage = usage
        self.project_name = project_name
        self.licence = gpl_licence.format(usage, str(year), name, project_name)

    def make_isc_licence(self, name: str, year: int):
        self.name = name
        self.year = year
        self.licence = isc_licence.format(str(year), name)

    class LicenceNotFound(Exception):
        def __init__(self, message="Licence not found"):
            self.message = message
            super().__init__(self.message)


if __name__ == "__main__":
    App().mainloop()
