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
        self.do_work = ttk.Button(self, text="Set-up and Run", command=self.do_work)
        self.main_title.pack()
        self.do_work.pack()
        self.mainloop()

    def count_down(self, count_time: int):
        """
        Count down
        Args:
            count_time: int: Wait seconds
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
        sec = easygui.enterbox("How many seconds do you want to count down?\nEach beep represents the passage of a second.\nPress OK to work, press Cancel to terminate the action.")
        if (sec != None != ""):
            self.count_down(int(sec))

    class Beep:
        @staticmethod
        def windows_beep(): winsound.Beep(1440, 200)
        # Whistle, frequency 1440Hz, lasts 200ms

        @staticmethod
        def unix_beep(): os.system("play --no-show-progress --null --channels 1 synth 0.2 sine 1440")
        # Whistle, frequency 1440Hz, lasts 200ms

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
            # At the end, the buzzer rings six times in a row


if __name__ == "__main__":
    App()
