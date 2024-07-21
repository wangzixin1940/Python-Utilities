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
    print("""Usage:
python / py clear.py [/l] [/c] [/p] [/?]
/l : Clear all logs
/c : Clear all caches
/p : Erases all profiles
------------------------------------
/l /c /p : Clear all
/? : Show help information
------------------------------------
ERROR: No arguments provided.
""")
    exit(1)

if "/l" in argvs:
    clear_logs()

if "/c" in argvs:
    clear_caches()

if "/p" in argvs:
    config = input(
        "OK to erase profile? Input \"0000\" confirm the action. NOTE: that this operation is irreversible!")
    if config == "0000":
        clear_profiles()
    else:
        print("This action was not taken(/p)。")

if "/?" in argvs:
    print("""Usage:
python / py clear.py [/l] [/c] [/p] [/?]
/l : Clear all logs
/c : Clear all caches
/p : Erases all profiles
------------------------------------
/l /c /p : Clear all
/? : Show help information
""")

if "/l" not in argvs and "/c" not in argvs and "/p" not in argvs:
    print("""Usage:
python / py clear.py [/l] [/c] [/p] [/?]
/l : Clear all logs
/c : Clear all caches
/p : Erases all profiles
------------------------------------
/l /c /p : Clear all
/? : Show help information
------------------------------------
ERROR: the parameter is incorrect
""")
    exit(2)

exit(0)
