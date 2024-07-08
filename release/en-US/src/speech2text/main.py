import ttkbootstrap as ttk
from tkinter import filedialog as fdg
from tkinter import messagebox as msgbox
import threading
import convert

MODELS = [
    "vosk-model-small-en-us-0.15",
    "vosk-model-en-us-0.22",
    "vosk-model-en-us-0.22-lgraph",
    "vosk-model-en-us-0.42-gigaspeech",
    "vosk-model-en-us-daanzu-20200905",
    "vosk-model-en-us-daanzu-20200905-lgraph",
    "vosk-model-en-us-librispeech-0.2",
    "vosk-model-small-en-us-zamia-0.5",
    "vosk-model-en-us-aspire-0.2",
    "vosk-model-en-us-0.21",
    "vosk-model-en-in-0.5",
    "vosk-model-small-en-in-0.4",
    "vosk-model-small-cn-0.22",
    "vosk-model-cn-0.22",
    "vosk-model-cn-kaldi-multicn-0.15",
    "vosk-model-ru-0.42",
    "vosk-model-small-ru-0.22",
    "vosk-model-ru-0.22",
    "vosk-model-ru-0.10",
    "vosk-model-small-fr-0.22",
    "vosk-model-fr-0.22",
    "vosk-model-small-fr-pguyot-0.3",
    "vosk-model-fr-0.6-linto-2.2.0",
    "vosk-model-de-0.21",
    "vosk-model-de-tuda-0.6-900k",
    "vosk-model-small-de-zamia-0.3",
    "vosk-model-small-de-0.15",
    "vosk-model-small-es-0.42",
    "vosk-model-es-0.42",
    "vosk-model-small-pt-0.3",
    "vosk-model-pt-fb-v0.1.1-20220516_2113",
    "vosk-model-el-gr-0.7",
    "vosk-model-small-tr-0.3",
    "vosk-model-small-vn-0.4",
    "vosk-model-vn-0.4",
    "vosk-model-small-it-0.22",
    "vosk-model-it-0.22",
    "vosk-model-small-nl-0.22",
    "vosk-model-nl-spraakherkenning-0.6",
    "vosk-model-nl-spraakherkenning-0.6-lgraph",
    "vosk-model-small-ca-0.4",
    "vosk-model-ar-mgb2-0.4",
    "vosk-model-ar-0.22-linto-1.1.0",
    "vosk-model-small-fa-0.4",
    "vosk-model-fa-0.5",
    "vosk-model-small-fa-0.5",
    "vosk-model-tl-ph-generic-0.6",
    "vosk-model-small-uk-v3-nano",
    "vosk-model-small-uk-v3-small",
    "vosk-model-uk-v3",
    "vosk-model-uk-v3-lgraph",
    "vosk-model-small-kz-0.15",
    "vosk-model-kz-0.15",
    "vosk-model-small-sv-rhasspy-0.15",
    "vosk-model-small-ja-0.22",
    "vosk-model-ja-0.22",
    "vosk-model-small-eo-0.42",
    "vosk-model-small-hi-0.22",
    "vosk-model-hi-0.22",
    "vosk-model-small-cs-0.4-rhasspy",
    "vosk-model-small-pl-0.22",
    "vosk-model-small-uz-0.22",
    "vosk-model-small-ko-0.22",
    "vosk-model-br-0.8",
    "vosk-model-gu-0.42",
    "vosk-model-small-gu-0.42",
    "vosk-model-tg-0.22",
    "vosk-model-small-tg-0.22",
    "vosk-model-spk-0.4",
    "vosk-recasepunc-en-0.22",
    "vosk-recasepunc-ru-0.22",
    "vosk-recasepunc-de-0.21",
]
# 查看更多，请前往 https://alphacephei.com/vosk/models
# Visit https://alphacephei.com/vosk/models for more

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        # Create window
        self.title("Speech to text converter")
        self.geometry("400x300")
        self.resizable(False, False)
        self.styleset = ttk.Style("cosmo")
        # self.iconbitmap("assets/favicon.ico")
        self.styleset.configure("TButton", font=("Airal", 16, "normal"), width=15, height=3)
        # Create widgets
        self.maintitle = ttk.Label(self, text="Speech to text converter", font=("Airal", 20, "bold"))
        self.file = ttk.StringVar(self, value="Choose audio file")
        self.filechoose = ttk.Button(self, textvariable=self.file, bootstyle="primary-outline", command=self.choose_file)
        self.modelchoose = ttk.Combobox(self, values=MODELS, width=15, font=("Airal", 16, "normal"))
        self.convert = ttk.Button(self, text="Convert", bootstyle="success-outline", command=self.convert_file)
        # Pack widgets
        self.maintitle.pack(pady=10)
        self.filechoose.pack(pady=10)
        self.modelchoose.pack(pady=10)
        self.convert.pack(pady=10)
    
    def choose_file(self):
        self.file.set(fdg.askopenfilename(filetypes=[("Wave audio files", "*.wav")]))
    
    def convert_file(self):
        if self.file.get() != "Choose audio file":
            convert.convert(self.file.get(), self.modelchoose.get())
        else:
            msgbox.showerror("Error", "Please choose an audio file first!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
