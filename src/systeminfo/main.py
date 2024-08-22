import platform
import datetime
import logging

import os
os.chdir(os.path.dirname(__file__))
# Change working directory to the current file's directory

import json

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["system_info"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]

logging.basicConfig(
    filename=f"../../logs/{datetime.date.today()}.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SYSINFO")
# Configure logging


class Functions:
    def __init__(self):
        super().__init__()

    @staticmethod
    def show_choices():
        for line in ui["choices"]:
            print(line)

    @staticmethod
    def match_choice_and_run(choice):
        if (platform.system() == "Windows"):
            os.system("cls")
        else:
            os.system("clear")
        match choice:
            case "1":
                print(f"{ui["system_class"]["architecture"]} {platform.architecture()}")
            case "2":
                print(f"{ui["system_class"]["machine"]} {platform.machine()}")
            case "3":
                print(f"{ui["system_class"]["platform"]} {platform.platform()}")
            case "4":
                print(f"{ui["system_class"]["cpu"]} {platform.processor()}")
            case "5":
                print(f"{ui["system_class"]["release"]} {platform.release()}")
            case "6":
                print(f"{ui["system_class"]["name"]} {platform.system()}")
            case "7":
                print(f"{ui["system_class"]["machine_name"]} {platform.node()}")
            case "8":
                print(f"{ui["system_class"]["windows_edition"]} {platform.win32_edition()}")
            case "9":
                print(f"{ui["system_class"]["mac_version"]} {platform.mac_ver()}")
            case "0":
                print(f"{ui["system_class"]["freedesktop_os_release"]} {platform.freedesktop_os_release()}")
            case "a":
                print(f"{ui["python_class"]["build"]} {platform.python_build()}")
            case "b":
                print(f"{ui["python_class"]["compiler"]} {platform.python_compiler()}")
            case "c":
                print(f"{ui["python_class"]["implementation"]} {platform.python_implementation()}")
            case "d":
                print(f"{ui["python_class"]["python_version"]} {platform.python_version()}")
            case "e":
                print(f"{ui["python_class"]["jpython_ver"]} {platform.java_ver()}")
            case "ab":
                for line in ui["about_text"]:
                    print(line)
            case "x":
                return 1
            case _:
                print(ui["error_option"])
        return 0


def main():
    functions = Functions()
    while True:
        functions.show_choices()
        choice = input(ui["input_option"])
        try:
            result = functions.match_choice_and_run(choice)
            logger.info(f"User chose option {choice} .")
            if result == 1:
                break
        except KeyboardInterrupt:
            print(ui["interrupt"])
            logger.warning("User cancelled operation.")
            break
        except Exception as e:
            print(ui["error_occurred"].format(err=repr(e)))
            logger.error(f"Error occurred: {repr(e)}")


if __name__ == "__main__":
    main()
