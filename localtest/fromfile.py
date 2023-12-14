import os
import azure.cognitiveservices.speech as speechsdk

def from_file():
    sub = os.environ.get('SPEECH_KEY')
    reg = os.environ.get('SPEECH_REGION')
    speech_config = speechsdk.SpeechConfig(sub, reg)
    audio_input = speechsdk.AudioConfig(filename="D:/cosas uni/cosasDePython/TelegramBOT/localtest/file_0.opus")
    
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once_async().get()
    print(result.text)

from_file()