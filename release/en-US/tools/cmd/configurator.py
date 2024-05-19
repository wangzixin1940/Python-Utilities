import sys
import os
import json
import ttkbootstrap

os.chdir(os.path.dirname(__file__))

themes = ttkbootstrap.Style().theme_names()
themes.append("pride")

def main():
    if len(sys.argv) <= 2:
        print(f"""Usage:
python / py configurator.py /theme [theme_name]
theme_name: Theme name, any of {themes}. It must be used in conjunction with the \"/theme\" parameter
--------------------------------------------------------------
ERROR: No parameters are given. Only given {len(sys.argv)-1} parameters.
""")
        return 1
    elif len(sys.argv) == 3:
        if sys.argv[2] in themes:
            try:
                with open("../../data/theme.json", "w", encoding="utf-8") as f:
                    json.dump({"theme": sys.argv[2]}, f, ensure_ascii=False, indent=4)
                    print(f"The theme has been set to \"{sys.argv[2]}\"")
                    return 0
            except FileNotFoundError:
                print("Profile not found. Fixes are needed you can go to GitHub to download the latest version of the \"theme.json\" file.")
                return -1
        else:
            print(f"ERROR: Unknown theme \"{sys.argv[2]}\"。")
            return 2
    else:
        print(f"""Usage:
python / py configurator.py /theme [theme_name]
theme_name: Theme name, any of {themes}. It must be used in conjunction with the \"/theme\" parameter
--------------------------------------------------------------
ERROR: too many parameters. Given {len(sys.argv)-1} parameters.
""")
        return 3

if __name__ == "__main__":
    sys.exit(main())