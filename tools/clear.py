import shutil
import pathlib
import ttkbootstrap as ttk
from tkinter import messagebox as msgbox

import os
import json

os.chdir(os.path.dirname(__file__))
# 更换工作目录

with open("../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["tools"]["clear"]["gui"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


def clear_logs():
    log_path = "../logs/"
    files = os.listdir(log_path)
    for file in files:
        file_path = os.path.join(log_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")
    print("All log files have been deleted.")
    msgbox.showinfo(ui_src["info"], ui["infos"]["log"])


def clear_caches():
    cache_path = pathlib.Path("../../")
    files = list(cache_path.rglob("__pycache__"))
    if len(files) != 0:
        for dir in files:
            shutil.rmtree(dir)
        print("All cache files have been deleted.")
    else:
        print("Cache files not found.")
    msgbox.showinfo(ui["info"], ui["infos"]["pycache"])


def clear_profiles():
    result = msgbox.askyesno(ui_src["warn"], ui["infos"]["userDataWarning"], icon="warning")
    if result:
        with open("../data/theme.json", "w", encoding="utf-8") as f:
            f.write("{\"theme\": \"cosmo\"}")
        os.remove("../data/translator.appid.json")
        print("User data has been reset.")
        clear_logs()
        print("Deleted all log files")
        clear_caches()
        print("Deleted all cache files")
        msgbox.showinfo(ui_src["info"], ui["infos"]["userData"])


def main():
    root = ttk.Window(themename="cosmo")
    root.title(ui["title"])
    root.geometry("350x300")
    root.resizable(False, False)
    title_label = ttk.Label(root, text=ui["title"], font=("Arial", 20, "bold"))
    clear_log = ttk.Button(root, text=ui["buttons"]["log"], command=clear_logs, bootstyle="primary-outline")
    clear_cache = ttk.Button(root, text=ui["buttons"]["pycache"], command=clear_caches, bootstyle="primary-outline")
    clear_profile = ttk.Button(root, text=ui["buttons"]["userData"], command=clear_profiles, bootstyle="danger-outline")
    title_label.pack(pady=20)
    clear_log.pack(pady=10)
    clear_cache.pack(pady=10)
    clear_profile.pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
