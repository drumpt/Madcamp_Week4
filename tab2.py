import main
import tab1

import sys
import time
import copy

import cv2
from PyQt5.QtCore import *
from PyQt5 import QtGui
# from PyQt5 import QtM
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tensorflow.keras.models import load_model


class SecondTab(QWidget):
    def __init(self):
        print("Hi")
        super().__init__()
