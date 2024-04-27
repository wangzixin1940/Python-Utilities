import sys
import os
import json
import ttkbootstrap

os.chdir(os.path.dirname(__file__))

themes = ttkbootstrap.Style().theme_names()

def main():
    if len(sys.argv) <= 2:
        print(f"""用法:
python / py configurator.py /theme [theme_name]
theme_name: 主题名称，{themes}的任意一个，必须和/theme参数并用
--------------------------------------------------------------
错误：未给出参数，仅给出了{len(sys.argv)-1}个参数。
""")
        return 1
    elif len(sys.argv) == 3:
        if sys.argv[2] in themes:
            try:
                with open("../../data/theme.json", "w", encoding="utf-8") as f:
                    json.dump({"theme": sys.argv[2]}, f, ensure_ascii=False, indent=4)
                    print(f"已将主题设置为\"{sys.argv[2]}\"")
                    return 0
            except FileNotFoundError:
                print("未找到配置文件。需要进行修复。可以去GitHub下载最新版本的theme.json。")
                return -1
        else:
            print(f"错误：未知的主题\"{sys.argv[2]}\"。")
            return 2
    else:
        print(f"""用法:
python / py configurator.py /theme [theme_name]
theme_name: 主题名称，{themes}的任意一个，必须和/theme参数并用
--------------------------------------------------------------
错误：参数过多，给出了{len(sys.argv)-1}个参数。
""")
        return 3

if __name__ == "__main__":
    sys.exit(main())