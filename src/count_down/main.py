import platform
import time
import ttkbootstrap as ttk
import easygui

if (platform.system() == "Windows"):
    import winsound
    mode = 1
else:
    import os
    mode = 0


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Count Down Timer")
        self.geometry("300x200")
        self.resizable(False, False)
        self.style_set = ttk.Style("cosmo")
        self.style_set.configure("TButton", width=15, font=("Airal", 14, "normal"))
        self.main_title = ttk.Label(self, text="Count Down Timer", font=("Airal", 18, "bold"))
        self.do_work = ttk.Button(self, text="设置并运行", command=self.do_work)
        self.main_title.pack()
        self.do_work.pack()
        self.mainloop()

    def count_down(self, count_time: int):
        """
        倒计时
        Args:
            count_time: int: 等待秒数
        """
        if mode:
            for i in range(1, count_time + 1):
                self.Beep.windows_beep()
                print(str(i) + "s")
                time.sleep(0.8)
        else:
            for i in range(count_time):
                self.Beep.unix_beep()
                print(str(i) + "s")
                time.sleep(0.8)
        self.Beep.done(mode)

    def do_work(self):
        sec = easygui.enterbox("您要倒计时多少秒？\n每一次蜂鸣都代表过去了一秒。\n按确定工作，按取消终止操作。")
        if (sec != None != ""):
            self.count_down(int(sec))

    class Beep:
        @staticmethod
        def windows_beep(): winsound.Beep(1440, 200)
        # 鸣笛，频率1440Hz，持续200ms

        @staticmethod
        def unix_beep(): os.system("play --no-show-progress --null --channels 1 synth 0.2 sine 1440")
        # 鸣笛，频率1440Hz，持续200ms

        @staticmethod
        def done(mode: int):
            for i in range(2):
                if (mode == 1):
                    for j in range(3):
                        winsound.Beep(1440, 50)
                else:
                    for j in range(3):
                        os.system("play --no-show-progress --null --channels 1 synth 0.05 sine 1440")
                time.sleep(0.1)
            # 结束时，蜂鸣器连续响六下


if __name__ == "__main__":
    App()
