import pypinyin
import ttkbootstrap as ttk


def query(word):
    """
    查询一个汉字的拼音（该功能仅限中文版）
    Args:
        word: 汉字
    Returns:
        拼音
    """
    return (pypinyin.pinyin(word, style=pypinyin.TONE, v_to_u=True), pypinyin.pinyin(word, style=pypinyin.BOPOMOFO, v_to_u=True))
    # 输出拼音和注音，带声调，将字符中的v替换为ü(ㄩ)


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("汉字拼音字典")
        self.geometry("500x500")
        self.resizable(False, False)
        self.style_set = ttk.Style(theme="cosmo")
        self.style_set.configure("TButton", font=("微软雅黑", 12), width=20)
        self.main_title = ttk.Label(self, text="汉字拼音字典", font=("微软雅黑", 20))
        self.main_title.grid(columnspan=2, pady=10, row=0)
        self.entry_label = ttk.Label(self, text="请输入一个\n或多个汉字：", font=("微软雅黑", 12, "normal"))
        self.entry_label.grid(column=0, row=1, padx=10, pady=10)
        self.entry_text = ttk.Entry(self, width=20, font=("微软雅黑", 12, "normal"))
        self.entry_text.grid(column=1, row=1, padx=10, pady=10)
        self.query_button = ttk.Button(self, text="查询", command=self.processing, bootstyle="success-outline")
        self.query_button.grid(columnspan=2, row=2, padx=10, pady=10)
        self.pinyin = ttk.StringVar(value="拼音：未知")
        self.zhuyin = ttk.StringVar(value="注音：未知")
        self.pinyin_label = ttk.Label(self, textvariable=self.pinyin, font=("微软雅黑", 14, "normal"))
        self.pinyin_label.grid(columnspan=2, row=3, padx=10, pady=10)
        self.zhuyin_label = ttk.Label(self, textvariable=self.zhuyin, font=("微软雅黑", 14, "normal"))
        self.zhuyin_label.grid(columnspan=2, row=4, padx=10, pady=10)
        self.mainloop()

    def processing(self):
        result = query(self.entry_text.get())  # type: tuple[list[list[str]]]
        result_pinyin = ""
        for i in result[0]:
            result_pinyin += i[0] + " "
        self.pinyin.set("拼音：" + result_pinyin)
        ########################
        result_zhuyin = ""
        for i in result[1]:
            result_zhuyin += i[0] + " "
        self.zhuyin.set("注音：" + result_zhuyin)


if __name__ == '__main__':
    App()
