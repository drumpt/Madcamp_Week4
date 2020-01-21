import os

import main
import pygame
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
# import my_magenta


class StartDialog():
    def __init(self):
        super().__init()

    @property
    def cat_index(self):
        return self.__cat_index

    @cat_index.setter
    def cat_index(self, index):
        self.__cat_index = index

    def setupUi(self, Dialog):
        #
        # # my_magenta 실행
        # exec('my_magenta')


        self.__cat_index = -1
        self.__musicThread = MusicPlay()
        self.__musicThread.play()

        Dialog.setObjectName("Dialog")
        Dialog.setGeometry(600, 300, 640, 480)
        Dialog.setStyleSheet("background-image: url(./tab1_photo/bgi.jpg); font-family:'배달의민족 주아'; src:'BMJUA_ttf.ttf'")
        Dialog.setWindowTitle("다재다냥★♬")

        self.start_btn = QPushButton(Dialog)
        self.start_btn.setGeometry(240, 85, 180, 180)
        start_icon = QtGui.QIcon('./tab1_photo/git.png')
        self.start_btn.setIcon(start_icon)
        self.start_btn.setIconSize(QtCore.QSize(180, 180))
        self.start_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        self.start_btn.clicked.connect(lambda: self.second(Dialog))

        # 로고
        self.logo_img = QPixmap()
        self.logo_img.load("./tab1_photo/logo_1.png")
        self.logo_img = self.logo_img.scaled(QSize(500, 130))
        self.logo_label = QLabel(Dialog)
        self.logo_label.setPixmap(self.logo_img)
        self.logo_label.show()
        self.logo_label.setGeometry(85, 280, 500, 130)

    def second(self, Dialog):
        # 냥이 선택 창
        print("클릭됨")
        self.select_cat("next", Dialog)

        self.logo_label.hide()
        self.start_btn.hide()

        self.title = QLabel(Dialog)
        _translate = QtCore.QCoreApplication.translate
        self.title.setText(_translate("Dialog", "가장 마음에 드는 펫을 선택하세요"))
        self.title.setFont(QtGui.QFont('배달의민족 주아', 15))
        self.title.setStyleSheet("Color: rgb(30,30,30)")
        self.title.setGeometry(190, 45, 300, 50)
        self.title.show()


        # previous 버튼
        self.previous_btn = QPushButton(Dialog)
        self.previous_btn.setGeometry(65, 190, 80, 80)
        previous_icon = QtGui.QIcon('./tab1_photo/previous.png')
        self.previous_btn.setIcon(previous_icon)
        self.previous_btn.setIconSize(QtCore.QSize(80, 80))
        self.previous_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.previous_btn.show()

        # next 버튼
        self.next_btn = QPushButton(Dialog)
        self.next_btn.setGeometry(490, 190, 80, 80)
        next_icon = QtGui.QIcon('./tab1_photo/next.png')
        self.next_btn.setIcon(next_icon)
        self.next_btn.setIconSize(QtCore.QSize(80, 80))
        self.next_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.next_btn.show()


        # 시작 버튼
        self.select_btn = QPushButton(Dialog)
        self.select_btn.setGeometry(QtCore.QRect(500, 440, 60, 30))
        # select_icon = QtGui.QIcon('next.png')
        # self.select_btn.setIcon(select_icon)
        # self.select_btn.setIconSize(QtCore.QSize(80, 80))
        # self.select_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.select_btn.setText("시작")
        self.select_btn.show()

        # 종료 버튼
        self.exit_btn = QPushButton(Dialog)
        self.exit_btn.setGeometry(QtCore.QRect(570, 440, 60, 30))
        # exit_icon = QtGui.QIcon('next.png')
        # self.exit_btn.setIcon(exit_icon)
        # self.exit_btn.setIconSize(QtCore.QSize(80, 80))
        # self.exit_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.exit_btn.setText("종료")
        self.exit_btn.show()

        # btn click slot
        self.next_btn.clicked.connect(lambda: self.select_cat("next", Dialog))
        self.previous_btn.clicked.connect(lambda: self.select_cat("previous", Dialog))
        self.exit_btn.clicked.connect(Dialog.reject)
        self.select_btn.clicked.connect(lambda: self.startMainwindow(Dialog))

        # self.select_btn.clicked.connect(self.actionCustomFactors, SIGNAL("triggered()"), self.OnCustomFactorsTriggered)

    # def OnCustomFactorsTriggered(self):
    #     self.customWin = main.mainWindow()
    #     self.customWin.show()
    #     self.connect(self.customWin, SIGNAL("closed()"), self.OnCustomWinClosed)

    def startMainwindow(self, Dialog):
        Dialog.reject()
        print("Hi 1")
        self.newWindow = main.mainWindow()
        print("Hi 2")
        self.newWindow.init_window()
        print("Hi 3")
        self.newWindow.tab1.add_init_box(self.img_path)
        self.newWindow.tab2.setupUi()
        self.__musicThread.stop()

    # 냥이 사진 select
    def select_cat(self, part, Dialog):

        img_path = "./images"
        cat_list = os.listdir(img_path)
        # index 계산
        if part == "previous":
            if self.__cat_index == 0:  # 맨 첫번째인데 previous
                self.__cat_index = len(cat_list) - 1
            else:
                self.__cat_index -= 1

        elif part == "next":
            if self.__cat_index == (len(cat_list) - 1):  # 맨 마지막인데 next
                self.__cat_index = 0
            else:
                self.__cat_index += 1

        img_path = img_path + "/" + cat_list[self.__cat_index]
        self.img_path = img_path

        print("인덱스 " + str(self.__cat_index))
        print(img_path)

        # 캐릭터 보여주기
        self.cat_imgs = QPixmap()
        self.cat_imgs.load(img_path)
        # self.cat_imgs = QImage.fromData(open(img_path, "rb").read(), 'jpg')
        self.cat_imgs = self.cat_imgs.scaled(250, 250)

        self.cat_label = QLabel(Dialog)
        # self.cat_label.setImage(self.cat_imgs)
        self.cat_label.setPixmap(self.cat_imgs)
        self.cat_label.show()
        self.cat_label.setGeometry(190, 110, 250, 250)

        self.cat_txtname = QLabel(Dialog)
        file_name = cat_list[self.__cat_index]
        cat_name = file_name[:-4]
        print(cat_name)
        self.cat_txtname.setText(cat_name)
        # self.cat_txtname.setStyleSheet(" { font-family: 'Malgun Gothic'; background-color: rgba(255, 255, 255, 0%);}")
        self.cat_txtname.setStyleSheet("background-color: rgba(255, 255, 255, 0); Color: rgb(30,30,30)")
        self.cat_txtname.setAlignment(QtCore.Qt.AlignHCenter)
        self.cat_txtname.setFont(QtGui.QFont('배달의민족 주아', 15))
        self.cat_txtname.setGeometry(190, 387, 250, 30)
        self.cat_txtname.show()


class MusicPlay():
    def __init__(self):
        # super(MusicPlay, self).__init__(parent)
        music_file = "./test1.mid"
        self.music_file = music_file

    def play(self):
        # pygame.mixer.Sound(self.music_file)
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(1)

        try:
            pygame.mixer.music.load(self.music_file)
            print(" %s 로드" % self.music_file)
        except pygame.error:
            print(" %s 에러 (%s)" % (self.music_file, pygame.get_error()))
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()
