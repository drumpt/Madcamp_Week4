# import main

from PyQt5 import QtGui
from PyQt5.QtCore import *
# from PyQt5 import QtM
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class ThirdTab(QWidget):
    def __init(self):
        super().__init__()

    def init_window(self):
        # gif 전체 화면
        self.start_cat = QMovie('./tab3_photo/catStart.gif')
        self.start_cat.setScaledSize(QSize(640, 480))
        self.cat_label = QLabel(self)
        self.cat_label.setMovie(self.start_cat)
        self.cat_label.show()
        self.cat_label.setGeometry(0, 0, 640, 480)
        self.movie = self.start_cat
        self.start_cat.start()

        # Layout
        self.form_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        self.setLayout(self.form_layout)

        # 버튼
        self.start_btn = QPushButton(self)
        upload_icon = QtGui.QIcon('./tab3_photo/transparent.png')
        self.start_btn.setIcon(upload_icon)
        # self.start_btn.setIconSize(QSize(640, 480))
        # self.start_btn.setGeometry(0, 0, 640, 480)
        self.start_btn.setIconSize(QSize(450, 350))
        self.start_btn.setGeometry(0, 0, 450, 350)
        self.start_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.start_btn.show()
        self.start_btn.clicked.connect(lambda: self.sketchpad_start())

        self.form_layout.addWidget(self.start_btn)

    # sketchpad 시작
    def sketchpad_start(self):
        print("클릭됨")
        self.start_btn.hide()
        self.cat_label.hide()
        self.web = QWebEngineView()
        self.web.load(QUrl("https://magic-sketchpad.glitch.me/"))
        self.web.setGeometry(0, 0, 640, 480)
        self.form_layout.addWidget(self.web)
