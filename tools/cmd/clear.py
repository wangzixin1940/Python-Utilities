import sys
import os
import pathlib
import shutil

os.chdir(os.path.dirname(__file__))


def clear_logs():
    log_path = "../../logs/"
    files = os.listdir(log_path)
    for file in files:
        file_path = os.path.join(log_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")
    print("All log files have been deleted.")


def clear_caches():
    cache_path = pathlib.Path("../../")
    files = list(cache_path.rglob("__pycache__"))
    if len(files) != 0:
        for dir in files:
            shutil.rmtree(dir)
        print("All cache files have been deleted.")
    else:
        print("Cache files not found.")


def clear_profiles():
    with open("../../data/theme.json", "w", encoding="utf-8") as f:
        f.write("{\"theme\": \"cosmo\"}")
        print("Rewrited theme.json")
    os.remove("../../data/translator.appid.json")
    print("Deleted translator.appid.json")
    clear_logs()
    clear_caches()


argvs = sys.argv

if len(argvs) <= 1:
    print("""用法:
python / py clear.py [/l] [/c] [/p] [/?]
/l : 清除所有日志
/c : 清除所有缓存
/p : 清除所有配置文件
------------------------------------
/l /c /p : 清除所有
/? : 显示帮助信息
------------------------------------
错误：未给出参数
""")
    exit(1)

if "/l" in argvs:
    clear_logs()

if "/c" in argvs:
    clear_caches()

if "/p" in argvs:
    config = input("是否清除所有配置文件？输入0000确认操作。注意，此操作不可逆！")
    if config == "0000":
        clear_profiles()
    else:
        print("未执行此操作(/p)。")

if "/?" in argvs:
    print("""用法:
python / py clear.py [/l] [/c] [/p] [/?]
/l : 清除所有日志
/c : 清除所有缓存
/p : 清除所有配置文件
------------------------------------
/l /c /p : 清除所有
/? : 显示帮助信息
""")

if "/l" not in argvs and "/c" not in argvs and "/p" not in argvs:
    print("""用法:
python / py clear.py [/l] [/c] [/p] [/?]
/l : 清除所有日志
/c : 清除所有缓存
/p : 清除所有配置文件
------------------------------------
/l /c /p : 清除所有
/? : 显示帮助信息
------------------------------------
错误：参数不正确
""")
    exit(2)

exit(0)
