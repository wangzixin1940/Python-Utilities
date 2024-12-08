from difflib import HtmlDiff
import tkinter.filedialog as fdg
import socket
import dicttoxml
import xmltodict
import threading
import subprocess
import random
import urllib
import hashlib
import http.client
from PIL import Image
import requests
import platform
import datetime
import logging
import easygui
import ttkbootstrap as ttk
from tkinter import messagebox as msgbox
import os
import json

with open("data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=settings["encoding"])
# Change the encoding of the standard output


os.chdir(os.path.dirname(__file__))
# Change the working directory to the directory of the script

with open(settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)  # type: dict[str: dict]

if not (settings["no-log-file"]):
    logging.basicConfig(
        filename=f"logs/{datetime.date.today()}.log",
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
logger = logging.getLogger("ROOT")
# Configure the logger





class System():
    @staticmethod
    def about():
        msgbox.showinfo(title="Python Utilities", message=ui["system"]["about"])

    @staticmethod
    def languageSettings():
        filepath = fdg.askopenfilename(title="Select Language File", filetypes=[("JSON Files", "*.json")],
                                       defaultextension="*.json")
        if (filepath):
            if (msgbox.askokcancel(title="Windows Utilities",
                                   message=f"You chose the file \"{filepath}\".\n" +
                                           "Are you sure you want to use this file?" +
                                           "Make sure this profile is complete and don't delete it in the future" +
                                           "(unless you change it).")):
                settings["language"] = filepath
                with open("data/settings.json", "w", encoding="utf-8") as file:
                    json.dump(settings, file, indent=4, ensure_ascii=False)
                    if (easygui.buttonbox(title="Windows Utilities",
                                          msg="You'll have to restart the program to apply the changes.",
                                          choices=["Restart Now", "Restart later"], default_choice="Restart Now",
                                          cancel_choice="Restart later") == "Restart Now"):
                        root.destroy()
                        os.system("python main.py")

    @staticmethod
    def quitApp():
        root.destroy()

    def switchTheme(theme_name):
        if (theme_name == "pride"):
            root.iconbitmap("./images/pride.ico")
            style.theme_use("cosmo")
            style.configure("TButton", font=(
                "Helvetica", 18, "normal"), width=20, height=3)
            style.configure("TMenubutton", font=(
                "Helvetica", 18, "normal"), width=19, height=3)
        else:
            root.iconbitmap("./images/icon.ico")
            style.theme_use(theme_name)
            style.configure("TButton", font=(
                "Helvetica", 18, "normal"), width=20, height=3)
            style.configure("TMenubutton", font=(
                "Helvetica", 18, "normal"), width=19, height=3)
        theme["theme"] = theme_name
        with open("./data/theme.json", "w") as f:
            json.dump(theme, f)

    @staticmethod
    def importSettings():
        path = easygui.fileopenbox(title=ui["system"]["importSettings"]["open"], filetypes=[
            ["*.json", "JSON files"]], default="*.json")
        global settings
        if (path != None):
            if (msgbox.askokcancel(title="Python Utilities",
                                   message=ui["system"]["importSettings"]["warning"],
                                   icon="warning")):
                with open(path, "r+", encoding="utf-8") as new_settings:
                    new_settings = new_settings.read()
                    new_settings = json.loads(new_settings)
                    logger.info(f"Settings: {new_settings}")
                    with open("data/settings.json", "w+", encoding="utf-8") as settings:
                        settings.write(json.dumps(
                            new_settings, ensure_ascii=False, indent=4))
                        msgbox.showinfo(
                            title="Python Utilities", message=ui["system"]["importSettings"]["complete"])
                        logger.info("Settings imported")


def main(*args):
    global root
    global style
    global theme
    root = ttk.Window()
    try:
        root.wm_attributes(*args)
    except Exception as e:
        logger.error(repr(e))
    with open("./data/theme.json", "r", encoding="utf-8") as theme:
        theme = theme.read()
        theme = json.loads(theme)
    root.title("Python Utilities")
    root.geometry("{}x{}".format(
        settings["geometry"][0], settings["geometry"][1]))
    root.resizable(settings["resizable"][0], settings["resizable"][1])
    if settings["icon-file-path"] == "@default":
        if theme["theme"] == "pride":
            root.iconbitmap("./images/pride.ico")
            style = ttk.Style("cosmo")
        else:
            root.iconbitmap("./images/icon.ico")
            style = ttk.Style(theme["theme"])
    else:
        if os.path.exists(settings["icon-file-path"]):
            root.iconbitmap(settings["icon-file-path"])
            style = ttk.Style("cosmo")
        else:
            root.iconbitmap("./images/icon.ico")
            style = ttk.Style("cosmo")
            logger.warning(
                "Icon file not found. Program will use default icon and cosmo theme.")
    style.configure("TButton", font=(
        "Helvetica", 18, "normal"), width=20, height=3)
    style.configure("TMenubutton", font=(
        "Helvetica", 18, "normal"), width=19, height=3)
    # Window
    main_ui_src = ui["ui"]
    menu_src = ui["ui"]["menus"]
    # ===================================== #
    title = ttk.Label(root, text="Python Utilities",
                      font=("Helvetica", 22, "normal"))
    title.pack()  # The title of this program
    # ===================================== #
    utilitiesLabel = ttk.Label(
        root, text=main_ui_src["utilities"]["title"], font=("Helvetica", 18, "normal"))
    utilitiesLabel.pack()  # Utilities label
    translateButton = ttk.Button(text=main_ui_src["utilities"]["translator"],
                                 command=Launcher.DevToolsLauncher.translatorLauncher,
                                 bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    translateButton.pack()  # Translator button
    weatherButton = ttk.Button(root, text=main_ui_src["utilities"]["weatherReport"],
                               command=Launcher.ExternalLauncher.weatherLauncher,
                               bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    weatherButton.pack()  # Weather forecast button
    speech2textButton = ttk.Button(root, text=main_ui_src["utilities"]["speech2text"],
                                   command=Launcher.ExternalLauncher.speech2textLauncher,
                                   bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    speech2textButton.pack()  # Speech-to-text button
    doWorkButton = ttk.Button(root, text=main_ui_src["utilities"]["to-do"],
                              command=Launcher.ExternalLauncher.doWorkLauncher,
                              bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    doWorkButton.pack()  # Easy To Do button
    # ===================================== #
    DevToolsLabel = ttk.Label(root, text=main_ui_src["dev"]["title"],
                              font=("Helvetica", 18, "normal"))
    DevToolsLabel.pack()  # Developer Tools label
    connectButton = ttk.Button(text=main_ui_src["dev"]["connectInformation"],
                               command=Launcher.DevToolsLauncher.webConnectTestLauncher,
                               bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    connectButton.pack()  # Detect network connections
    # speedTestButton = ttk.Button(root, text=main_ui_src["dev"]["speedtest"],
    #                               command=Launcher.ExternalLauncher.webSpeedTestLauncher,
    #                              bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    # speedTestButton.pack()  # Speed test button (deprecated)
    # ===================================== #
    externalsLabel = ttk.Label(
        root, text=main_ui_src["others"]["title"], font=("Helvetica", 18, "normal"))
    externalsLabel.pack()  # Other Tools tabs
    passwordCreatorButton = ttk.Button(root, text=main_ui_src["others"]["passwordCreator"],
                                       command=Launcher.ExternalLauncher.passwordCreatorLauncher,
                                       bootstyle=(ttk.PRIMARY, ttk.OUTLINE))
    passwordCreatorButton.pack()  # Password generator button
    # ===================================== #
    if not (settings["no-menu"]):
        menu = ttk.Menu(root)
        fileMenu = ttk.Menu(menu)
        otherMenu = ttk.Menu(menu)
        settingsMenu = ttk.Menu(menu)
        menu.add_cascade(label=menu_src["file"]["title"], menu=fileMenu)
        menu.add_cascade(label=menu_src["other"]["title"], menu=otherMenu)
        if not (settings["no-settings-menu"]):
            menu.add_cascade(label=menu_src["settings"]["title"], menu=settingsMenu)
        menu.add_command(label=menu_src["about"], command=System.about)
        fileMenu.add_command(label=menu_src["file"]["importSettings"], command=System.importSettings)
        fileMenu.add_command(label=menu_src["file"]["exit"], command=System.quitApp)
        otherMenu.add_command(
            label=menu_src["other"]["calculator"], command=Launcher.ExternalLauncher.calculatorLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["hashChecker"], command=Launcher.ExternalLauncher.hashCheckerLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["licenceCreator"], command=Launcher.ExternalLauncher.licenceCreatorLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["smfj"], command=Launcher.ExternalLauncher.sendMailFromJSONLauncher)
        ipToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label=menu_src["other"]["ipTools"]["title"], menu=ipToolsMenu)
        ipToolsMenu.add_command(
            label=menu_src["other"]["ipTools"]["getIP"], command=Launcher.DevToolsLauncher.getIPLauncher)
        ipToolsMenu.add_command(
            label=menu_src["other"]["ipTools"]["resolveDomain"],
            command=Launcher.DevToolsLauncher.resolveDomainLauncher)
        fileToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label=menu_src["other"]["fileTools"]["title"], menu=fileToolsMenu)
        fileToolsMenu.add_command(
            label=menu_src["other"]["fileTools"]["jsonToXml"], command=Launcher.DevToolsLauncher.JSONtoXMLLauncher)
        fileToolsMenu.add_command(
            label=menu_src["other"]["fileTools"]["xmlToJson"], command=Launcher.DevToolsLauncher.XMLtoJSONLauncher)
        fileToolsMenu.add_command(
            label=menu_src["other"]["fileTools"]["jsonToCsv"], command=Launcher.DevToolsLauncher.JSONtoCSVLauncher)
        fileToolsMenu.add_command(
            label=menu_src["other"]["fileTools"]["csvToJson"], command=Launcher.DevToolsLauncher.CSVtoJSONLauncher)
        fileToolsMenu.add_command(label=menu_src["other"]["fileTools"]["diff"], command=DevTools.FileDiffTools)
        qrcodeToolsMenu = ttk.Menu(otherMenu)
        otherMenu.add_cascade(label=menu_src["other"]["qrcodeTools"]["title"], menu=qrcodeToolsMenu)
        qrcodeToolsMenu.add_command(
            label=menu_src["other"]["qrcodeTools"]["generate"],
            command=Launcher.ExternalLauncher.qrcodeGeneratorLauncher)
        qrcodeToolsMenu.add_command(
            label=menu_src["other"]["qrcodeTools"]["parse"], command=Launcher.ExternalLauncher.qrcodeParserLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(
            label=menu_src["other"]["asciiArt"], command=Launcher.DrawingToolsLauncher.charPictureLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["bingPicture"], command=Launcher.DrawingToolsLauncher.bingPictureLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["pictureConvertor"],
            command=Launcher.ExternalLauncher.pictureFormatConverterLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["amk"], command=Launcher.ExternalLauncher.AMKLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["captcha"], command=Launcher.ExternalLauncher.captchaLauncher)
        otherMenu.add_separator()
        otherMenu.add_command(
            label=menu_src["other"]["clock"], command=Launcher.ExternalLauncher.clockLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["countDown"], command=Launcher.ExternalLauncher.countDownLauncher)
        otherMenu.add_command(
            label=menu_src["other"]["pinyinDictionary"], command=Launcher.ExternalLauncher.pinyinLauncher)
        if not (settings["no-settings-menu"]):
            themesMenu = ttk.Menu(settingsMenu)
            settingsMenu.add_cascade(label=menu_src["settings"]["themes"], menu=themesMenu)
            for i in style.theme_names():
                themesMenu.add_radiobutton(
                    label=i, command=lambda name=i: System.switchTheme(name)
                )
            themesMenu.add_separator()
            themesMenu.add_command(
                label="pride", command=lambda: System.switchTheme("pride"))
            settingsMenu.add_command(
                label="Choose language profile", command=System.languageSettings)
        root.config(menu=menu)
    # Toolbar
    # ===================================== #
    root.mainloop()
