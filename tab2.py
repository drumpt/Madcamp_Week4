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
        self.setStyleSheet("QWidget {background-color: white;}")
        self.show()

    def setupUi(self):
        self.setGeometry(600, 300, 640, 480)

        movie = QMovie('./tab2_photo/Cat_Dance4.gif')
        movie.setScaledSize(QSize(170, 200))
        music_label = QLabel(self)
        music_label.setMovie(movie)
        music_label.show()
        music_label.setGeometry(10, 10, 170, 200)
        self.movie = movie
        movie.start()
        movie.loopCount()

        initBox = QTextEdit(self)
        initBox.setText("당신의 음악을 편곡해드릴게요!")
        initBox.setStyleSheet("QTextEdit {background-color: rgb(241, 241, 241); border-radius: 10px; padding: 10px;}")
        initBox.setAlignment(Qt.AlignVCenter)
        initBox.setGeometry(200, 40, 250, 56)
        initBox.setReadOnly(True)
        self.initBox = initBox
        initBox.show()

        self.play_btn = QPushButton(self)
        play_icon = QtGui.QIcon('./tab2_photo/download_icon.png')
        self.play_btn.setIcon(play_icon)
        self.play_btn.setIconSize(QSize(50, 50))
        self.play_btn.setGeometry(240, 150, 50, 50)
        # self.play_btn.setStyleSheet("{background-color: red;}")
        self.play_btn.show()
        self.play_btn.clicked.connect(lambda: self.play_btn_clicked())

    def play_btn_clicked(self):
        self.fname = QFileDialog.getOpenFileName(self)[0]
        print(self.fname)

        # 편곡 로직

        # 결과 음악 실행 - ./test1.mid(이름 변경)
        self.music_on = MusicPlay()
        self.music_on.play()


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
