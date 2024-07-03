import platform
import datetime
import logging

import os
os.chdir(os.path.dirname(__file__))
# Change directory to current file

logging.basicConfig(
                    filename=f"../../logs/{datetime.date.today()}.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SYSINFO")
# Configure logger

class Functions:
    def __init__(self):
        super().__init__()

    def show_choices(self):
        print("""
System Infomation Viewer V 1.0
========================================================
System Part
1. System architecture\t2. Machine type\t3. System version\t4. Processor (CPU) name\t5. System release\t6. System name
7. The name of the computer on the network\t8. Windows Editon(e.g. Professional、Home Basic) (Windows only)
9. Mac system infomation (macOS only)\t0. Linux system infomation (Linux only)
About Python
a. Python compile code and compile date\tb. Python compiler version\tc. Python implementer identity\td. Python version
e. Jython version of the interface (Jython only)
Software
ab. About\tx. Exit
""")

    def match_choice_and_run(self, choice):
        match choice:
            case "1":
                print(f"System architecture: {platform.architecture()}")
            case "2":
                print(f"Machine type: {platform.machine()}")
            case "3":
                print(f"System version: {platform.platform()}")
            case "4":
                print(f"Processor (CPU) name: {platform.processor()}")
            case "5":
                print(f"System release: {platform.release()}")
            case "6":
                print(f"System name: {platform.system()}")
            case "7":
                print(f"The name of the computer on the network: {platform.node()}")
            case "8":
                print(f"Windows version: {platform.win32_edition()}")
            case "9":
                print(f"Mac system infomation: {platform.mac_ver()}")
            case "0":
                print(f"Linux system infomation: {platform.freedesktop_os_release()}")
            case "a":
                print(f"Python compile code and compile date: {platform.python_build()}")
            case "b":
                print(f"Python compiler version: {platform.python_compiler()}")
            case "c":
                print(f"Python implementer identity: {platform.python_implementation()}")
            case "d":
                print(f"Python version: {platform.python_version()}")
            case "e":
                print(f"Jython version of the interface: {platform.java_ver()}")
            case "ab":
                print("""
About the system information viewer
========================================================
The system information viewer is a tool for viewing system information. 
The system information viewer is written in Python and uses the platform module of python to obtain system information.
""")
            case "x":
                return 1
            case _:
                print("Invalid option. Please re-enter.")
        return 0

def main():
    functions = Functions()
    while True:
        functions.show_choices()
        choice = input("Input choice  >>> ")
        try :
            result = functions.match_choice_and_run(choice)
            logger.info(f"User chose option {choice} .")
            if result == 1:
                break
        except KeyboardInterrupt:
            print("The user canceled the action.")
            logger.warning("User cancelled operation.")
            break
        except Exception as e:
            print(f"Error occurred：{repr(e)}")
            logger.error(f"Error occurred: {repr(e)}")

if __name__ == "__main__":
    main()


