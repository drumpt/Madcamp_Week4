# import main

import pygame
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
# from PyQt5 import QtM
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FourthTab():
    def __init(self):
        super().__init__()

    def init_window(self):
        self.setGeometry(0, 0, 640, 480)
        self.setStyleSheet("QWidget {background-color: white; background-image: url(./tab4_photo/main.png)}")
        self.show()