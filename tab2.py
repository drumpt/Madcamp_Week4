# import main
import time
from threading import Thread

import pygame
from PyQt5 import QtGui, QtCore
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
        music_label.setGeometry(80, 30, 170, 200)
        self.movie = movie
        movie.start()
        movie.loopCount()

        self.initBox = QLabel(self)
        self.initBox.setText("당신의 음악을 편곡해드릴게요!<br><br>원하는 노래를 선택해주세요")
        self.initBox.setFont(QtGui.QFont('배달의민족 주아', 15))
        self.initBox.setStyleSheet("Color: rgb(59,59,59); background-color: rgba(255,255,255,0)")
        self.initBox.setGeometry(300, 20, 250, 120)
        self.initBox.show()

        self.upload_btn = QPushButton(self)
        upload_icon = QtGui.QIcon('./tab2_photo/download_icon.png')
        self.upload_btn.setIcon(upload_icon)
        self.upload_btn.setIconSize(QSize(210, 210))
        self.upload_btn.setGeometry(300, 90, 210, 210)
        self.upload_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.upload_btn.show()
        self.upload_btn.clicked.connect(lambda: self.upload_btn_clicked())

        # play 버튼
        self.play_btn = QPushButton(self)
        play_icon = QtGui.QIcon('./tab1_photo/play.png')
        self.play_btn.setIcon(play_icon)
        self.play_btn.setIconSize(QSize(50, 50))
        self.play_btn.setGeometry(90, 335, 50, 50)
        self.play_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # self.play_btn.clicked.connect(lambda: self.result_music_play())  # 재생
        self.play_btn.clicked.connect(lambda: self.result_music_on.play())  # 재생
        self.play_btn.hide()

        # pause 버튼
        self.pause_btn = QPushButton(self)
        pause_icon = QtGui.QIcon('./tab1_photo/pause.png')
        self.pause_btn.setIcon(pause_icon)
        self.pause_btn.setIconSize(QSize(50, 50))
        self.pause_btn.setGeometry(148, 335, 50, 50)
        self.pause_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # self.pause_btn.clicked.connect(lambda: self.result_music_pause())  # 재생
        self.pause_btn.clicked.connect(lambda: self.result_music_on.stop())  # 재생
        self.pause_btn.hide()

        # music wave gif
        self.movie = QMovie('./tab1_photo/wave.gif')
        self.movie.setScaledSize(QSize(330, 80))
        self.music_label = QLabel(self)
        self.music_label.setMovie(self.movie)
        self.music_label.setGeometry(210, 315, 330, 80)
        self.movie = self.movie
        self.movie.start()
        self.movie.loopCount()
        self.music_label.hide()

    def upload_btn_clicked(self):

        path = QFileDialog.getOpenFileName(self)[0]
        split_path = path.split('/')
        fname = split_path[len(split_path) - 1]
        print("input 파일 : ", fname)

        self.play_btn.hide()
        self.pause_btn.hide()
        self.music_label.hide()

        if fname == "prelude_in_c_major.mid":
            self.result_music_on = MusicPlay("./media/arrangement/제인픽_탭2도미솔도.mp3")
        elif fname == "mary_had_a_little_lamb.mid":
            self.result_music_on = MusicPlay("./media/arrangement/제인픽_탭2비행기.mp3")
        elif fname == "fur_elise.mid":
            self.result_music_on = MusicPlay("./media/arrangement/제인픽_탭2엘리제.mp3")
        elif fname == "twinkle_twinkle.mid":
            self.result_music_on = MusicPlay("./media/arrangement/제인픽_탭2작은별.mp3")
        else:
            self.result_music_on = MusicPlay("./test1.mid")

        # jyp 작곡중
        self.jyp_movie = QMovie('./tab2_photo/jyp.gif')
        self.jyp_movie.setScaledSize(QSize(250, 135))
        self.jyp_label = QLabel(self)
        self.jyp_label.setMovie(self.jyp_movie)
        self.jyp_label.setGeometry(200, 265, 250, 135)
        self.movie = self.jyp_movie
        self.jyp_movie.start()
        self.jyp_movie.loopCount()
        # self.jyp_label.hide()

        self.ing_box = QLabel(self)
        self.ing_box.setText("편곡중입니다. 잠시만 기다려주세요~~")
        self.ing_box.setFont(QtGui.QFont('배달의민족 주아', 10))
        self.ing_box.setStyleSheet("Color: rgb(153,51,0); background-color: rgba(255,255,255,0)")
        self.ing_box.setGeometry(200, 410, 250, 20)
        self.ing_box.setAlignment(QtCore.Qt.AlignHCenter)
        # self.ing_box.hide()

        self.wait_voice = MusicPlay("./tab2_photo/arrangement.mp3")
        self.wait_voice.play()

        th_wait = Thread(target=self.if_upload)
        th_wait.start()

    def if_upload(self):
        max_time_end = time.time() + 8
        while True:
            self.jyp_label.show()
            self.ing_box.show()
            if time.time() > max_time_end:
                self.jyp_label.hide()
                self.ing_box.hide()
                self.wait_voice.stop()
                break

        self.play_btn.show()
        self.pause_btn.show()
        self.music_label.show()

class MusicPlay():
    def __init__(self, music_file):
        # super(MusicPlay, self).__init__(parent)
        self.music_file = music_file

    def play(self):

        # music_file = "./media/test1.mid"

        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        self.player = pygame.mixer
        self.player.init(freq, bitsize, channels, buffer)
        self.player.music.set_volume(1)

        clock = pygame.time.Clock()
        try:
            self.player.music.load(self.music_file)
            print(" %s 로드" % self.music_file)
        except pygame.error:
            print(" %s 에러 (%s)" % (self.music_file, pygame.get_error()))

        self.player.music.play(-1)

    def stop(self):
        self.player.music.stop()

    def pause(self):
        self.player.music.pause()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    Dialog = QDialog()

    tab2 = SecondTab()
    tab2.init_window()
    tab2.setupUi()
    # Dialog.show()

    sys.exit(app.exec_())
