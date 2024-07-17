import os
os.chdir(os.path.dirname(__file__))
# 将当前目录更改为脚本的目录

import logging
import datetime

logging.basicConfig(
                    filename=f"../../../logs/{datetime.date.today()}.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("TCZ")
# 配置logger

from pycorrector import Corrector
import ttkbootstrap as ttk

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("TextBlob")
        self.geometry("400x450")
        self.resizable(False, False)
        self.style_set = ttk.Style(theme="cosmo")
        self.style_set.configure("TButton", font=("Arial", 12), width=15)
        self.create_widgets()
        self.mainloop()
    
    def create_widgets(self):
        self.main_title = ttk.Label(self, text="文本改正", font=("Arial", 20))
        self.main_title.pack(pady=10)
        self.text_entry = ttk.ScrolledText(self, width=25, height=10)
        self.text_entry.pack(pady=10)
        self.analyze_button = ttk.Button(self, text="改正用法", command=self.analyze_text)
        self.analyze_button.pack(pady=10)
    
    def analyze_text(self):
        self.text_entry.configure(state="disabled")
        text = self.text_entry.get("1.0", "end")
        corrector = Corrector()
        results = corrector.correct_batch(text.splitlines()) # type: list[dict["source": str, "target": str, "errors": list[tuple[str, str, int]]]]
        self.text_entry.configure(state="normal")
        self.text_entry.delete("1.0", "end")
        for line in results:
            self.text_entry.insert("end", f"{line["target"]}\n")

if __name__ == "__main__":
    App()
