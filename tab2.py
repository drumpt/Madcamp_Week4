# import main

import pygame
from PyQt5 import QtGui
from PyQt5.QtCore import *
# from PyQt5 import QtM
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SecondTab(QWidget):
    def __init(self):
        super().__init__()

    def init_window(self):
        self.setWindowTitle('다재다냥')
        self.setGeometry(600, 300, 640, 480)
        self.setStyleSheet(
            "QWidget {background-color: white; background-image: url(./tab1_photo/bgi.jpg); font-family:'배달의민족 주아'; src:'BMJUA_ttf.ttf'}")
        self.show()

    def setupUi(self):
        self.setGeometry(600, 300, 640, 480)
        self.setStyleSheet(
            " {background-image: url(./tab1_photo/bgi.jpg); font-family:'배달의민족 주아'; src:'BMJUA_ttf.ttf'}")

        # 춤추는 냥이
        movie = QMovie('./tab2_photo/Cat_Dance4.gif')
        movie.setScaledSize(QSize(170, 200))
        music_label = QLabel(self)
        music_label.setMovie(movie)
        music_label.show()
        music_label.setGeometry(80, 55, 170, 200)
        self.movie = movie
        movie.start()
        movie.loopCount()

        self.initBox = QLabel(self)
        self.initBox.setText("당신의 음악을 편곡해드릴게요!<br><br>원하는 노래를 선택해주세요")
        self.initBox.setFont(QtGui.QFont('배달의민족 주아', 15))
        self.initBox.setStyleSheet("Color: rgb(59,59,59); background-color: rgba(255,255,255,0)")
        self.initBox.setGeometry(290, 45, 250, 120)
        self.initBox.show()

        self.upload_btn = QPushButton(self)
        upload_icon = QtGui.QIcon('./tab2_photo/download_icon.png')
        self.upload_btn.setIcon(upload_icon)
        self.upload_btn.setIconSize(QSize(210, 210))
        self.upload_btn.setGeometry(290, 120, 210, 210)
        self.upload_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.upload_btn.show()
        self.upload_btn.clicked.connect(lambda: self.play_btn_clicked())

    def play_btn_clicked(self):
        self.fname = QFileDialog.getOpenFileName(self)[0]
        print(self.fname)

        # 작곡중~
        self.jyp_movie = QMovie('./tab2_photo/jyp.gif')
        self.jyp_movie.setScaledSize(QSize(220, 135))
        self.jyp_label = QLabel(self)
        self.jyp_label.setMovie(self.jyp_movie)
        self.jyp_label.setGeometry(190, 280, 220, 135)
        self.movie = self.jyp_movie
        self.jyp_movie.start()
        self.jyp_movie.loopCount()
        self.jyp_label.show()

        # 편곡 로직
        # time.sleep(10)

        # 작곡중~ hide
        # self.jyp_label.hide()

        # 결과 음악 실행 - ./test1.mid(이름 변경)
        self.music_on = MusicPlay()
        self.music_on.play()

        # play 버튼
        self.play_btn = QPushButton(self)
        play_icon = QtGui.QIcon('./tab1_photo/play.png')
        self.play_btn.setIcon(play_icon)
        self.play_btn.setIconSize(QSize(50, 50))
        self.play_btn.setGeometry(125, 340, 50, 50)
        self.play_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # self.play_btn.clicked.connect(self.music_on.play())  # 재생
        self.play_btn.show()

        # music wave gif
        movie = QMovie('./tab1_photo/wave.gif')
        movie.setScaledSize(QSize(330, 80))
        music_label = QLabel(self)
        music_label.setMovie(movie)
        music_label.show()
        music_label.setGeometry(190, 325, 330, 80)
        self.movie = movie
        movie.start()
        movie.loopCount()


class MusicPlay():
    def __init__(self):
        # super(MusicPlay, self).__init__(parent)

        music_file = "./media/test1.mid"

        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        self.player = pygame.mixer
        self.player.init(freq, bitsize, channels, buffer)
        self.player.music.set_volume(1)

        clock = pygame.time.Clock()
        try:
            self.player.music.load(music_file)
            print(" %s 로드" % music_file)
        except pygame.error:
            print(" %s 에러 (%s)" % (music_file, pygame.get_error()))

    def play(self):
        self.player.music.play(1)

    def stop(self):
        self.player.music.stop()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    Dialog = QDialog()

    tab2 = SecondTab()
    tab2.init_window()
    tab2.setupUi()
    # Dialog.show()

    sys.exit(app.exec_())
