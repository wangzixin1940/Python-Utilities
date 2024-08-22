import hashlib
import sys
import time

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
    ui = json.loads(ui_src_file)["externals"]["tools"]["hash"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


def get_file_md5(fname):
    m = hashlib.md5()  # 创建md5对象
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象


def get_file_sha256(fname):
    m = hashlib.sha256()  # 创建sha256对象
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新sha256对象
    return m.hexdigest()  # 返回sha256对象


def get_file_sha1(fname):
    m = hashlib.sha1()  # 创建sha1对象
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新sha1对象
    return m.hexdigest()  # 返回sha1对象


def get_file_sha224(fname):
    m = hashlib.sha224()  # 创建sha224对象
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新sha224对象
    return m.hexdigest()  # 返回sha224对象


def main():
    argvs = sys.argv
    if len(argvs) > 5 or len(argvs) < 2:
        for line in ui["usage"]:
            print(line)
        print(ui["errors"]["param_count_err"])
        return 1
    filename = argvs[1].strip()
    if not os.path.isfile(filename):
        print(ui["file_not_found"])
        return 2
    if "--check" in argvs and len(argvs) == 5:
        if "-md5" == argvs[3]:
            value = argvs[4]
            if get_file_md5(filename) == value:
                print(ui["prompts"]["md5"]["correct"])
                print(ui["prompts"]["information"]["md5"], get_file_md5(filename))
            else:
                print(ui["prompts"]["md5"]["incorrect"])
                print(ui["prompts"]["information"]["md5"], get_file_md5(filename))
            return 0
        elif "-sha256" == argvs[3]:
            value = argvs[4]
            if get_file_sha256(filename) == value:
                print(ui["prompts"]["sha256"]["correct"])
                print(ui["prompts"]["information"]["sha256"], get_file_sha256(filename))
            else:
                print(ui["prompts"]["sha256"]["incorrect"])
                print(ui["prompts"]["information"]["sha256"], get_file_sha256(filename))
            return 0
        elif "-sha1" == argvs[3]:
            value = argvs[4]
            if get_file_sha1(filename) == value:
                print(ui["prompts"]["sha1"]["correct"])
                print(ui["prompts"]["information"]["sha1"], get_file_sha1(filename))
            else:
                print(ui["prompts"]["sha1"]["incorrect"])
                print(ui["prompts"]["information"]["sha1"], get_file_sha1(filename))
            return 0
        elif "-sha224" == argvs[3]:
            value = argvs[4]
            if get_file_sha224(filename) == value:
                print(ui["prompts"]["sha224"]["correct"])
                print(ui["prompts"]["information"]["sha224"], get_file_sha224(filename))
            else:
                print(ui["prompts"]["sha224"]["incorrect"])
                print(ui["prompts"]["information"]["sha224"], get_file_sha224(filename))
            return 0
        else:
            for line in ui["usage"]:
                print(line)
            print("param_err")
    elif "--check" in argvs and len(argvs) in [3, 4]:
        for line in ui["usage"]:
            print(line)
        print(ui["errors"]["required_param_missing_err"])
        return 3
    elif len(argvs) > 5:
        for line in ui["usage"]:
            print(line)
        print(ui["errors"]["param_count_too_many"])
        return 5
    elif len(argvs) == 2:
        print(ui["prompts"]["information"]["file_name"], filename)
        print(ui["prompts"]["information"]["file_size"], os.path.getsize(filename), "字节")
        print(ui["prompts"]["information"]["file_type"], os.path.splitext(filename)[1])
        print(
            ui["prompts"]["information"]["the_last_time_the_file_was_modified"],
            time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(
                    os.path.getmtime(filename))))
        print(ui["prompts"]["information"]["md5"], get_file_md5(filename))
        print(ui["prompts"]["information"]["sha256"], get_file_sha256(filename))
        print(ui["prompts"]["information"]["sha1"], get_file_sha1(filename))
        print(ui["prompts"]["information"]["sha224"], get_file_sha224(filename))
        return 0
    else:
        for line in ui["usage"]:
            print(line)
        print(ui["errors"]["unknown_err"])
        return 4


if __name__ == "__main__":
    sys.exit(main())
