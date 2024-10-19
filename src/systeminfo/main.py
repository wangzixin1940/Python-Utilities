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
    ui = json.loads(ui_src_file)["externals"]["systemInformation"]  # type: dict[str: str]
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
                print(f"{ui["systemClass"]["architecture"]} {platform.architecture()}")
            case "2":
                print(f"{ui["systemClass"]["machine"]} {platform.machine()}")
            case "3":
                print(f"{ui["systemClass"]["platform"]} {platform.platform()}")
            case "4":
                print(f"{ui["systemClass"]["cpu"]} {platform.processor()}")
            case "5":
                print(f"{ui["systemClass"]["release"]} {platform.release()}")
            case "6":
                print(f"{ui["systemClass"]["name"]} {platform.system()}")
            case "7":
                print(f"{ui["systemClass"]["machineName"]} {platform.node()}")
            case "8":
                print(f"{ui["systemClass"]["windowsEdition"]} {platform.win32_edition()}")
            case "9":
                print(f"{ui["systemClass"]["macVersion"]} {platform.mac_ver()}")
            case "0":
                print(f"{ui["systemClass"]["freedesktopOSRelease"]} {platform.freedesktopOSRelease()}")
            case "a":
                print(f"{ui["pythonClass"]["build"]} {platform.python_build()}")
            case "b":
                print(f"{ui["pythonClass"]["compiler"]} {platform.python_compiler()}")
            case "c":
                print(f"{ui["pythonClass"]["implementation"]} {platform.python_implementation()}")
            case "d":
                print(f"{ui["pythonClass"]["pythonVersion"]} {platform.pythonVersion()}")
            case "e":
                print(f"{ui["pythonClass"]["jpythonVersion"]} {platform.java_ver()}")
            case "ab":
                for line in ui["aboutText"]:
                    print(line)
            case "x":
                return 1
            case _:
                print(ui["errorOption"])
        return 0


def main():
    functions = Functions()
    while True:
        functions.show_choices()
        choice = input(ui["inputOption"])
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
            print(ui["errorOccurred"].format(err=repr(e)))
            logger.error(f"Error occurred: {repr(e)}")


if __name__ == "__main__":
    main()
