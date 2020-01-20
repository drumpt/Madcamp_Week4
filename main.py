import tab1
import tab2

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

class mainWindow(QWidget):
    def __init(self):
        super().__init()

    def init_window(self):
        self.setWindowTitle('Main window')
        self.setGeometry(600, 300, 640, 480)
        self.setStyleSheet("QWidget {background-color: white;}")

        self.tab1 = tab1.FirstTab()
        self.tab2 = tab2.SecondTab()

        tabwidget = QTabWidget()
        tabwidget.addTab(self.tab1, "First Tab")
        tabwidget.addTab(self.tab2, "Second Tab")

        vbox = QVBoxLayout()
        vbox.addWidget(tabwidget)

        self.setLayout(vbox)
        self.show()

        # sound = AudioSegment.from_file("C:/Users/q/Desktop/Week4/Program/twinkle_twinkle_melodyRNN.mid")
        # # sound.export("C:/Users/q/Desktop/Week4/Program/twinkle_twinkle_melodyRNN", format = "mp3", bitrate = "128k")
        # fruits = ['바나나', '사과', '멜론', '참외']
        # listview = QListView(self)
        # model = QStandardItemModel()
        # for fruit in fruits:
        #     model.appendRow(QStandardItem(fruit))
        # listview.setModel(model)

        # play_button = QPushButton("Play")
        # pause_button = QPushButton("Pause")
        # horizontal_box = QHBoxLayout()
        # horizontal_box.addwidget(play_button)
        # horizontal_box.addWidget(pause_button)
        # self.setLayout(horizontal_box)

    #     self.centralwidget = QtWidgets.QWidget(QMainWindow)
    #     self.centralwidget.setObjectName("centralwidget")
    #     self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
    #     self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 791, 551))
    #     self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
    #     self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
    #     self.verticalLayout.setContentsMargins(0, 0, 0, 0)
    #     self.verticalLayout.setObjectName("verticalLayout")
    #     self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
    #     self.pushButton.setObjectName("pushButton")
    #     self.verticalLayout.addWidget(self.pushButton)
    #     self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
    #     self.pushButton_2.setObjectName("pushButton_2")
    #     self.verticalLayout.addWidget(self.pushButton_2)
    #     QMainWindow.setCentralWidget(self.centralwidget)
    #     self.menubar = QtWidgets.QMenuBar(QMainWindow)
    #     self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 21))
    #     self.menubar.setObjectName("menubar")
    #     QMainWindow.setMenuBar(self.menubar)
    #     self.statusbar = QtWidgets.QStatusBar(QMainWindow)
    #     self.statusbar.setObjectName("statusbar")
    #     QMainWindow.setStatusBar(self.statusbar)
    #
    #     self.retranslateUi(QMainWindow)
    #     QtCore.QMetaObject.connectSlotsByName(QMainWindow)
    #
    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    #     self.pushButton.setText(_translate("MainWindow", "Play"))
    #     self.pushButton_2.setText(_translate("MainWindow", "Pause"))
    #     self.pushButton.clicked.connect(self.play)
    #     self.pushButton_2.clicked.connect(self.pause)
    #     self.url = QtCore.QUrl.fromLocalFile("C:/Users/q/Desktop/Week4/Program/twinkle_twinkle_melodyRNN.mp3")
    #     self.content = QtMultimedia.QMediaContent(self.url)
    #     self.player = QtMultimedia.QMediaPlayer()
    #     self.player.setMedia(self.content)
    #
    # def play(self):
    #     self.player.play()
    #
    # def pause(self):
    #     self.player.pause()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.init_window()
    window.tab1.add_init_box()
    window.tab1.add_answer_box()
    window.tab1.add_suggestion_box()
    window.tab1.add_response_box()
    sys.exit(app.exec_())