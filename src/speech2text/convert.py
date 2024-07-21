import datetime
import logging
from tkinter import messagebox as msgbox
import json
import vosk
import soundfile
import wave
import os
os.chdir(os.path.dirname(__file__))
# 更换工作目录


logging.basicConfig(
    filename=f"../../logs/{datetime.date.today()}.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SPEECH2TEXT")


vosk.SetLogLevel(0)


def convert(audio_path: wave.Wave_read, model_name: str):
    data, samplerate = soundfile.read(audio_path)
    soundfile.write(audio_path, data, samplerate)
    # 转为32位RIFF并且重新写入  |  Convert to 32-bit RIFF and rewrite
    audio = wave.open(audio_path, "rb")
    if (audio.getnchannels() != 1) or (audio.getsampwidth()
                                       != 2) or (audio.getcomptype() != "NONE"):
        logger.critical("Audio file must be WAV format mono PCM.")
        return
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
            logger.debug(result)
            result = json.loads(result)
            if "text" in result:
                str_ret += result["text"] + " "
            else:
                logger.debug(rec.PartialResult())
    result = json.loads(rec.FinalResult())
    if "text" in result:
        str_ret += result["text"]
    msgbox.showinfo("提示", "转换完成！\n结果：{}".format(str_ret))


"""
注意：
1. 音频文件必须是单声道、16位PCM编码的WAV文件。
2. 模型可以是以下几种：
    - "vosk-model-en-us-0.22-lgraph"
    - "vosk-model-small-cn-0.22"
    还有更多……
    具体在 https://alphacephei.com/vosk/models

Note:
1. The audio file must be a single-channel, 16-bit PCM-encoded WAV file.
2. The model can be one of the following:
    - "vosk-model-en-us-0.22-lgraph"
    - "vosk-model-small-cn-0.22"
    And more...
    See https://alphacephei.com/vosk/models for more details.

"""

# Debug:

# print(convert("test/1.wav", "vosk-model-en-us-0.22-lgraph"))
# print(convert("test/2.wav", "vosk-model-small-cn-0.22"))
