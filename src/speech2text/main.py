import vosk
import soundfile
import wave

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QStyleFactory, QMessageBox, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTranslator
from ui.s2t import Ui_MainWindow
import time
import sys

import os
import json

os.chdir(os.path.dirname(__file__))
# Change working directory to this file's directory

vosk.SetLogLevel(1)

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file


def convert(audio_path: wave.Wave_read, model_name: str):
    data, samplerate = soundfile.read(audio_path)
    soundfile.write(audio_path, data, samplerate)
    # Convert to 32-bit RIFF and rewrite
    audio = wave.open(audio_path, "rb")
    if (audio.getnchannels() != 1) or (audio.getsampwidth()
                                       != 2) or (audio.getcomptype() != "NONE"):
        return 1
    str_ret = ""
    model = vosk.Model(model_name=model_name)
    rec = vosk.KaldiRecognizer(model, audio.getframerate())
    rec.SetWords(True)
    while True:
        data = audio.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result = json.loads(result)
            if "text" in result:
                str_ret += result["text"] + " "
    result = json.loads(rec.FinalResult())
    if "text" in result:
        str_ret += result["text"]
    return str_ret


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect the buttons to the functions
        self.uploadAudioButton.clicked.connect(self.upload_audio)
        self.identifyButton.clicked.connect(self.identify)
        # Define the variables
        self.file_path = ""
        self.text = ""

    def upload_audio(self):
        self.file_path = QFileDialog.getOpenFileName(self, "Choose audio", "", "Wave Audio(*.wav)")[0]
        if self.file_path != "":
            self.uploadAudioButton.setText(self.file_path.split("/")[-1])

    def identify(self):
        if self.file_path == "":
            QMessageBox.critical(self, "Error", "Please choose a audio first!")
            return
        timer = time.time()
        self.text = convert(self.file_path, self.modelChooseCombo.currentText())
        # Convert the audio, the window will not respond and there is currently no solution :(
        QMessageBox.information(self, "Success", "Converted successfully. Time taken: " + str(round(time.time() - timer,
                                                                                                    2)) + "s")
        self.resultDisplay.setText(self.text)


if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    translator = QTranslator()
    if (translator.load(settings["qt_language"], directory="../../data/ui/i18n")):
        app.installTranslator(translator)
    window = App()
    window.setWindowIcon(QIcon("./assets/favicon.ico"))
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec())
