import main
import tab2

import sys
import time
import copy
import pygame
import time


import cv2
from PyQt5.QtCore import *
from PyQt5 import QtGui
# from PyQt5 import QtM
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tensorflow.keras.models import load_model

# for face detection
face_cascade = cv2.CascadeClassifier("C:/Users/q/Downloads/haarcascade_frontalface_alt.xml")
eye_cascade = cv2.CascadeClassifier("C:/Users/q/Downloads/haarcascade_eye_tree_eyeglasses.xml")
model = load_model("C:/Users/q/Downloads/another_model_2_10.h5", compile=False)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i
    return num

class FirstTab(QWidget):
    def __init__(self):
        super().__init__()

    def getPixmap(self, dir):
        if dir != "":
            image = QImage.fromData(open(dir, "rb").read(), 'jpg')
        else:
            print(self.face)
            face = cv2.cvtColor(self.face, cv2.COLOR_BGR2RGB)
            height, width, channel = face.shape
            image = QtGui.QImage(face.data, width, height, width * channel, QImage.Format_RGB888)
            # return image
        image.convertToFormat(QImage.Format_ARGB32)
        imgsize = min(image.width(), image.height())
        rect = QRect((image.width() - imgsize) / 2, (image.height() - imgsize) / 2, imgsize, imgsize)
        image = image.copy(rect)

        out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)

        brush = QBrush(image)  # Create texture brush
        painter = QPainter(out_img)  # Paint the output image
        painter.setBrush(brush)  # Use the image texture brush
        painter.setPen(Qt.NoPen)  # Don't draw an outline
        painter.setRenderHint(QPainter.Antialiasing, True)  # Use AA
        painter.drawEllipse(0, 0, imgsize, imgsize)  # Actually draw the circle
        painter.end()

        pr = QWindow().devicePixelRatio()
        pm = QPixmap.fromImage(out_img)
        pm.setDevicePixelRatio(pr)
        size = 56
        size *= pr
        pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pm

    def add_init_box(self):
        catLabel = QLabel(self)
        catLabel.setPixmap(self.getPixmap("./photo/로키.jpg"))
        catLabel.setGeometry(20, 20, 56, 56)
        # self.catLabel = catLabel
        catLabel.show()

        initBox = QTextEdit(self)
        initBox.setText("안녕하세요. 오늘 하루는 어떠셨나요? 당신의 기분이 궁금해요!")
        initBox.setStyleSheet("QTextEdit {background-color: rgb(241, 241, 241); border-radius: 10px; padding: 10px;}")
        initBox.setAlignment(Qt.AlignVCenter)
        initBox.setGeometry(90, 20, 250, 56)
        # initBox.setGeometry(20, 20, 250, 56)
        initBox.setReadOnly(True)
        initBox.show()

    def add_answer_box(self):
        class_to_emotion = {0: 'angry', 1: 'happy', 2: 'neutral', 3: 'sad', 4: 'surprise'}
        emotion_to_word = {"happy": "오늘 기뻤어.", "sad": "오늘 슬펐어.", "angry": "오늘 화났어.", "sleepy": "지금 졸려."}
        emotions = []

        cam = cv2.VideoCapture(0)
        cnt = 0

        while True:
            ret, frame = cam.read()
            frame = cv2.transpose(frame)
            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) >= 1:
                # print(len(faces))
                (x, y, w, h) = faces[0]
                # Find the largest face in the frame
                for i in range(len(faces)):
                    (xi, yi, wi, hi) = faces[i]
                    if wi * hi > w * h:
                        (x, y, w, h) = (xi, yi, wi, hi)
                eyes = eye_cascade.detectMultiScale(frame[y:y + h, x:x + w], scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
                if len(eyes) == 0:
                    emotions.append("sleepy")
                    cnt += 1
                    if cnt == 5:
                        self.face = frame[y:y + h, x: x+ w]
                else:
                    resized_face = cv2.cvtColor(cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
                    resized_frame = cv2.resize(resized_face, dsize=(48, 48), interpolation=cv2.INTER_AREA)
                    emotion = class_to_emotion[model.predict_classes(resized_frame.reshape([-1, 48, 48, 3]))[0]]
                    if emotion in ["happy", "sad", "angry"]:
                        emotions.append(emotion)
                        cnt += 1
                        if cnt == 5:
                            self.face = frame[y:y + h, x: x+ w]
                print(cnt)
                # cv2.putText(frame, emotion, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cv2.waitKey(100)

            # Display the resulting frame
            cv2.imshow('Face_to_emotion', frame)
            cv2.waitKey(1)

            if cnt >= 10 or cv2.waitKey(1) & 0xFF == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                break

        # emotion : happy, sad, angry, sleepy
        emotion = most_frequent(emotions)
        self.emotion = emotion
        print(emotion)

        faceLabel = QLabel(self)
        faceLabel.setPixmap(self.getPixmap(""))
        faceLabel.setGeometry(539, 114, 56, 56)
        # self.catLabel = catLabel
        faceLabel.show()

        answerBox = QTextEdit(self)
        answerBox.setText("나는 " + emotion_to_word[emotion])
        answerBox.setStyleSheet("QTextEdit {background-color: rgb(6, 136, 255); border-radius: 10px; padding: 10px; color: rgb(255, 255, 255)}")
        answerBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        answerBox.setGeometry(275, 100, 250, 42)
        answerBox.setReadOnly(True)
        answerBox.show()

    def add_suggestion_box(self): # 캐릭터 이름을 input으로 받을 수 있게 만들어야 함.
        emotion_to_word2 = {"happy": "기쁠", "sad": "슬플", "angry": "화날", "sleepy": "졸릴"}

        catLabel = QLabel(self)
        catLabel.setPixmap(self.getPixmap("./photo/로키.jpg"))
        catLabel.setGeometry(20, 166, 56, 56)
        catLabel.show()

        suggestionBox = QTextEdit(self)
        if self.emotion in ["happy", "sad"]:
            suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠!\n제가 직접 만들었어요ㅎㅎ"
        elif self.emotion == "angry":
            # suggestionText = emotion_to_word2[self.emotion]
            suggestionText = "분노와 교만에 지배되지 말아라. 그 뿌리를 뽑아 버려라.\n - 불경(佛經)"
        else: # sleepy
            # suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠ㅎㅎ"
            suggestionText = "절대로 고개를 떨구지 말라.\n고개를 들고 세상을 똑바로 바라보라."
        suggestionBox.setText(suggestionText)
        suggestionBox.setStyleSheet("QTextEdit {background-color: rgb(241, 241, 241); border-radius: 10px; padding: 10px; z-index: -1;}")
        suggestionBox.setAlignment(Qt.AlignVCenter)
        suggestionBox.setGeometry(90, 166, 250, 130)
        suggestionBox.setReadOnly(True)
        suggestionBox.show()

        self.__musicTread = MusicPlay()

        # 음악 재생 버튼
        self.__play_btn = QPushButton(self)
        play_icon = QtGui.QIcon('./tab1_photo/play.png')
        self.__play_btn.setIcon(play_icon)
        self.__play_btn.setIconSize(QSize(30, 30))
        self.__play_btn.setGeometry(105, 235, 30, 30)       # 65, 150, 110, 190
        self.__play_btn.setStyleSheet("{background-color: rgba(241, 241, 241, 0);}")
        self.__play_btn.show()

        # 음악 멈춤 버튼
        self.__stop_btn = QPushButton(self)
        stop_icon = QtGui.QIcon('./tab1_photo/pause.png')
        self.__stop_btn.setIcon(stop_icon)
        self.__stop_btn.setIconSize(QSize(30, 30))
        self.__stop_btn.setGeometry(105, 235, 30, 30)
        self.__stop_btn.setStyleSheet("{background-color: rgba(241, 241, 241, 0);}")
        self.__stop_btn.hide()

        # # 음악 재생 버튼
        # self.play_btn = QPushButton(self)
        # self.play_btn.setGeometry(65, 150, 110, 190)
        # play_icon = QtGui.QIcon('./tab1_photo/play.png')
        # self.play_btn.setIcon(play_icon)
        # self.play_btn.setIconSize(QSize(30, 30))
        # self.play_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # self.play_btn.show()
        #
        #
        # # 음악 멈춤 버튼
        # self.stop_btn = QPushButton(self)
        # self.stop_btn.setGeometry(65, 150, 110, 190)
        # stop_icon = QtGui.QIcon('./tab1_photo/pause.png')
        # self.stop_btn.setIcon(stop_icon)
        # self.stop_btn.setIconSize(QSize(30, 30))
        # self.stop_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # self.stop_btn.hide()


        # music wave
        try:
            movie = QMovie('./tab1_photo/wave.gif')  # , QByteArray(), self
            movie.setScaledSize(QSize(150,100))
            music_label = QLabel(self)
            music_label.setMovie(movie)
            music_label.show()
            music_label.setGeometry(150, 220, 150, 60)

            movie.start()
            movie.loopCount()
        except Exception as e:
            print(e)




        self.musicTread = MusicPlay()
        self.__play_btn.clicked.connect(lambda: self.music_play("play"))  # 재생
        self.__stop_btn.clicked.connect(lambda: self.music_pause("pause"))    # 멈춤

        # self.musicTread.start()
        # self.musicTread.
        # self.musicTread.stop()


    def music_play(self, part):
        if part == "play":
            self.__musicTread.start()
            self.__stop_btn.show()
            self.__play_btn.hide()

        elif part == "pause":


            self.__stop_btn.hide()
            self.__play_btn.show()


    # def music_pause(self):
    #     self.musicTread = MusicPlay()
    #     self.musicTread.start()



class MusicPlay(QThread):
    def __init__(self, parent=None):
        super(MusicPlay, self).__init__(parent)

    def run(self):

        path = "./media/"
        music_name = "test1.mid"
        music_file = path + music_name


        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(1)

        clock = pygame.time.Clock()
        try:
            pygame.mixer.music.load(music_file)
            print(" %s 로드" % music_file)
        except pygame.error:
            print(" %s 에러 (%s)" % (music_file, pygame.get_error()))

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)


