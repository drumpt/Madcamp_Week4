
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *


class FourthTab(QWidget):
    def __init(self):
        super().__init__()

    def init_window(self):
        self.start_btn = QPushButton(self)
        main_icon = QtGui.QIcon('./tab4_photo/main.png')
        self.start_btn.setIcon(main_icon)
        self.start_btn.setIconSize(QSize(640, 480))
        self.start_btn.setGeometry(0, 0, 640, 480)
        self.start_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.start_btn.show()
