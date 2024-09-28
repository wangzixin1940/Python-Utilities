import sys
import pathlib
import shutil

import os
import json

os.chdir(os.path.dirname(__file__))
# 更换工作目录

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["tools"]["clear"]["cli"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


def clear_logs():
    log_path = "../../logs/"
    files = os.listdir(log_path)
    for file in files:
        file_path = os.path.join(log_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")
    print(ui["infos"]["log"])


def clear_caches():
    cache_path = pathlib.Path("../../")
    files = list(cache_path.rglob("__pycache__"))
    if len(files) != 0:
        for dir in files:
            shutil.rmtree(dir)
        print(ui["infos"]["pycache"])
    else:
        print(ui["infos"]["pycacheNotFound"])


def clear_profiles():
    with open("../data/theme.json", "w", encoding="utf-8") as f:
        f.write("{\"theme\": \"cosmo\"}")
    os.remove("../data/translator.appid.json")
    clear_logs()
    clear_caches()
    print(ui["infos"]["userData"])


argvs = sys.argv

if len(argvs) <= 1:
    for line in ui["usage"]:
        print(line)
    print(ui["errors"]["paramsNotFound"])
    exit(1)

if "/l" in argvs:
    clear_logs()

if "/c" in argvs:
    clear_caches()

if "/p" in argvs:
    config = input(ui["infos"]["userDataWarning"])
    if config == "0000":
        clear_profiles()
    else:
        print(ui["infos"]["user_data_cancel"])

if "/?" in argvs:
    for line in ui["usage"]:
        print(line)

if "/l" not in argvs and "/c" not in argvs and "/p" not in argvs:
    for line in ui["usage"]:
        print(line)
    print(ui["errors"]["errorParam"])
    exit(2)

exit(0)
