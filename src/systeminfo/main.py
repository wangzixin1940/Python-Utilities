import platform
import datetime
import logging

import os
os.chdir(os.path.dirname(__file__))
# 更换工作目录

logging.basicConfig(
                    filename=f"../../logs/{datetime.date.today()}.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SYSINFO")
# 配置日志信息

class Functions:
    def __init__(self):
        super().__init__()

    def show_choices(self):
        print("""
系统信息查看器 V 1.0
========================================================
系统类
1. 系统架构\t2. 机器类型\t3. 系统版本\t4. 处理器(CPU)名称\t5. 系统发布版本\t6. 系统名称
7. 网络上计算机的名称\t8. Windows版本(比如Professional、Home Basic) (Windows 专用)
9. Mac系统信息 (macOS 专用)\t0. Linux 系统信息 (Linux 专用)
关于Python
a. Python编译代码和编译日期\tb. Python编译器版本\tc. Python实现器标识\td. Python版本
e. Jython 的版本接口 (Jython专用)
软件
ab. 关于\tx. 退出
""")

    def match_choice_and_run(self, choice):
        match choice:
            case "1":
                print(f"系统架构: {platform.architecture()}")
            case "2":
                print(f"机器类型: {platform.machine()}")
            case "3":
                print(f"系统版本: {platform.platform()}")
            case "4":
                print(f"处理器(CPU)名称: {platform.processor()}")
            case "5":
                print(f"系统发布版本: {platform.release()}")
            case "6":
                print(f"系统名称: {platform.system()}")
            case "7":
                print(f"网络上计算机的名称: {platform.node()}")
            case "8":
                print(f"Windows版本: {platform.win32_edition()}")
            case "9":
                print(f"Mac系统信息: {platform.mac_ver()}")
            case "0":
                print(f"Linux系统信息: {platform.freedesktop_os_release()}")
            case "a":
                print(f"Python编译代码和编译日期: {platform.python_build()}")
            case "b":
                print(f"Python编译器版本: {platform.python_compiler()}")
            case "c":
                print(f"Python实现器标识: {platform.python_implementation()}")
            case "d":
                print(f"Python版本: {platform.python_version()}")
            case "e":
                print(f"Jython的版本接口: {platform.java_ver()}")
            case "ab":
                print("""
关于系统信息查看器
========================================================
系统信息查看器是一个用于查看系统信息的工具。
系统信息查看器由Python编写，使用Python的platform模块获取系统信息。
""")
            case "x":
                return 1
            case _:
                print("无效的选项，请重新输入。")
        return 0

def main():
    functions = Functions()
    while True:
        functions.show_choices()
        choice = input("输入选项  >>> ")
        try :
            result = functions.match_choice_and_run(choice)
            logger.info(f"User chose option {choice} .")
            if result == 1:
                break
        except KeyboardInterrupt:
            print("用户已取消操作。")
            logger.warning("User cancelled operation.")
            break
        except Exception as e:
            print(f"发生错误：{repr(e)}")
            logger.error(f"Error occurred: {repr(e)}")

if __name__ == "__main__":
    main()


