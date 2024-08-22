import os
import json
os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["chinese_pinyin_dictionary"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]


import pypinyin
import ttkbootstrap as ttk


def query(word):
    """
    Query the pinyin of a Chinese character
    Args:
        word: Chinese character
    Returns:
        Pinyin
    """
    return (pypinyin.pinyin(word, style=pypinyin.TONE, v_to_u=True), pypinyin.pinyin(word, style=pypinyin.BOPOMOFO, v_to_u=True))
    # Output pinyin and zhuyin, with tones, replace v with ü (ㄩ)


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title(ui["title"])
        self.geometry("500x500")
        self.resizable(False, False)
        self.style_set = ttk.Style(theme="cosmo")
        self.style_set.configure("TButton", font=("Airal", 12), width=20)
        self.main_title = ttk.Label(self, text=ui["title"], font=("Airal", 20))
        self.main_title.grid(columnspan=2, pady=10, row=0)
        self.entry_label = ttk.Label(self, text=ui["input"], font=("Airal", 12, "normal"))
        self.entry_label.grid(column=0, row=1, padx=10, pady=10)
        self.entry_text = ttk.Entry(self, width=20, font=("Airal", 12, "normal"))
        self.entry_text.grid(column=1, row=1, padx=10, pady=10)
        self.query_button = ttk.Button(self, text=ui["query"], command=self.processing, bootstyle="success-outline")
        self.query_button.grid(columnspan=2, row=2, padx=10, pady=10)
        self.pinyin = ttk.StringVar(value=ui["pinyin"]+ui["unknown"])
        self.zhuyin = ttk.StringVar(value=ui["zhuyin"]+ui["unknown"])
        self.pinyin_label = ttk.Label(self, textvariable=self.pinyin, font=("Airal", 14, "normal"))
        self.pinyin_label.grid(columnspan=2, row=3, padx=10, pady=10)
        self.zhuyin_label = ttk.Label(self, textvariable=self.zhuyin, font=("Airal", 14, "normal"))
        self.zhuyin_label.grid(columnspan=2, row=4, padx=10, pady=10)
        self.mainloop()

    def processing(self):
        result = query(self.entry_text.get())  # type: tuple[list[list[str]]]
        result_pinyin = ""
        for i in result[0]:
            result_pinyin += i[0] + " "
        self.pinyin.set(ui["pinyin"] + result_pinyin)
        ########################
        result_zhuyin = ""
        for i in result[1]:
            result_zhuyin += i[0] + " "
        self.zhuyin.set(ui["zhuyin"] + result_zhuyin)


if __name__ == '__main__':
    App()
