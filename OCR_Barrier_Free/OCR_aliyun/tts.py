from PyQt5.QtCore import QThread
import pyttsx3


class TTSThread(QThread):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text

    def run(self):
        engine = pyttsx3.init()
        engine.say(self.text)
        engine.runAndWait()

