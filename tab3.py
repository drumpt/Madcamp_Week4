# import main
import time

import pygame
from PyQt5 import QtGui
from PyQt5.QtCore import *
# from PyQt5 import QtM
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class ThirdTab(QWebEngineView):
    def __init(self):
        super().__init__()

    def init_window(self):
        self.load(QUrl("https://magic-sketchpad.glitch.me/"))
        self.show()