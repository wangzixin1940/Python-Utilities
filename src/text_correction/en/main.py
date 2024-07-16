import os
os.chdir(os.path.dirname(__file__))
# Change the current directory to the directory of the script

class ModuleDownloadFailedWarning(Warning):
    def __init__(self, message):
        super().__init__(message)
    
    def __str__(self):
        return {self.args[0]}

import logging
import datetime

logging.basicConfig(
                    filename=f"../../../logs/{datetime.date.today()}.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("TCE")
# Config the logger

import nltk
import warnings
responses = []
packages = ["punkt", "averaged_perceptron_tagger", "brown", "wordnet"]
for package in packages:
    if package not in nltk.data.path:
        responses.append(nltk.download(package))
for response in range(len(responses)):
    if not(responses[response]):
        logger.warning("Error download package: {}".format(packages[response]))
        warnings.warn("Error download package: {}".format(packages[response]), ModuleDownloadFailedWarning)
# Download NLTK data

from textblob import TextBlob
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
        self.main_title = ttk.Label(self, text="TextBlob", font=("Arial", 20))
        self.main_title.pack(pady=10)
        self.text_entry = ttk.ScrolledText(self, width=25, height=10)
        self.text_entry.pack(pady=10)
        self.analyze_button = ttk.Button(self, text="Analyze", command=self.analyze_text)
        self.analyze_button.pack(pady=10)
    
    def analyze_text(self):
        self.text_entry.configure(state="disabled")
        text = self.text_entry.get("1.0", "end")
        blob = TextBlob(text)
        blob.correct()
        self.text_entry.configure(state="normal")
        self.text_entry.delete("1.0", "end")
        self.text_entry.insert("1.0", blob.correct())

if __name__ == "__main__":
    App()
