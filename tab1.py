import main
import tab2

import sys
import time
import copy
import os
import random

import cv2
from PyQt5.QtCore import *
from PyQt5 import QtGui
# from PyQt5 import QtM
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tensorflow.keras.models import load_model
import pygame

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
    def __init(self):
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

    def add_init_box(self, img_path):
        self.img_path = img_path
        # def restart():
        #     global self
        #     self.restartButton.hide()
        #     self.catLabel1.hide()
        #     self.initBox.hide()
        #     self.faceLabel1.hide()
        #     self.answerBox.hide()
        #     self.catLabel2.hide()
        #     self.suggestionBox.hide()
        #     self.faceLabel2.hide()
        #     self.responseBox.hide()
        #     self.okayButton.hide()
        #     self.refreshButton.hide()
        #     # self.hide()
        #     self = FirstTab()
        #     self.add_init_box()
        #     self.add_answer_box()
        #     self.add_suggestion_box()
        #     self.add_response_box()

        # restartButton = QPushButton('', self)
        # restartButton.setIcon(QIcon("./photo/restart.jpg"))
        # restartButton.setIconSize(QSize(30, 30))
        # restartButton.setGeometry(574, 10, 30, 30)
        # restartButton.clicked.connect(lambda: restart())
        # self.restartButton = restartButton
        # restartButton.show()

        catLabel = QLabel(self)
        catLabel.setPixmap(self.getPixmap(self.img_path))
        catLabel.setGeometry(20, 20, 56, 56)
        self.catLabel1 = catLabel
        catLabel.show()

        initBox = QTextEdit(self)
        initBox.setText("안녕하세요. 오늘 하루는 어떠셨나요? 당신의 기분이 궁금해요!")
        initBox.setStyleSheet("QTextEdit {background-color: rgb(241, 241, 241); border-radius: 10px; padding: 10px;}")
        initBox.setAlignment(Qt.AlignVCenter)
        initBox.setGeometry(90, 20, 250, 56)
        # initBox.setGeometry(20, 20, 250, 56)
        initBox.setReadOnly(True)
        self.initBox = initBox
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
                    if cnt == 1:
                        self.face = frame[y:y + h, x: x+ w]
                else:
                    resized_face = cv2.cvtColor(cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
                    resized_frame = cv2.resize(resized_face, dsize=(48, 48), interpolation=cv2.INTER_AREA)
                    emotion = class_to_emotion[model.predict_classes(resized_frame.reshape([-1, 48, 48, 3]))[0]]
                    if emotion in ["happy", "sad", "angry"]:
                        emotions.append(emotion)
                        cnt += 1
                        if cnt == 1:
                            self.face = frame[y:y + h, x: x+ w]
                print(cnt)
                # cv2.putText(frame, emotion, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cv2.waitKey(100)

            # Display the resulting frame
            cv2.imshow('Face_to_emotion', frame)
            cv2.waitKey(1)

            if cnt >= 3 or cv2.waitKey(1) & 0xFF == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                break

        # emotion : happy, sad, angry, sleepy
        emotion = most_frequent(emotions)
        self.emotion = emotion
        print(emotion)

        faceLabel = QLabel(self)
        faceLabel.setPixmap(self.getPixmap(""))
        faceLabel.setGeometry(539, 100, 56, 56)
        self.faceLabel1 = faceLabel
        faceLabel.show()

        answerBox = QTextEdit(self)
        answerBox.setText("나는 " + emotion_to_word[emotion])
        answerBox.setStyleSheet("QTextEdit {background-color: rgb(6, 136, 255); border-radius: 10px; padding: 10px; color: rgb(255, 255, 255)}")
        answerBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        answerBox.setGeometry(275, 114, 250, 42)
        # answerBox.setGeometry(275, 100, 250, 42)
        answerBox.setReadOnly(True)
        self.answerBox = answerBox
        answerBox.show()

    def add_suggestion_box(self): # 캐릭터 이름을 input으로 받을 수 있게 만들어야 함.
        emotion_to_word2 = {"happy": "기쁠", "sad": "슬플", "angry": "화날", "sleepy": "졸릴"}

        catLabel = QLabel(self)
        catLabel.setPixmap(self.getPixmap(self.img_path))
        catLabel.setGeometry(20, 195, 56, 56)
        self.catLabel2 = catLabel
        catLabel.show()

        suggestionBox = QTextEdit(self)
        if self.emotion in ["happy", "sad"]:
            suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠!\n제가 직접 만들었어요ㅎㅎ"
        elif self.emotion == "angry":
            # suggestionText = emotion_to_word2[self.emotion]
            suggestionText = "분노와 교만에 지배되지 말아라.\n그 뿌리를 뽑아 버려라. - 불경(佛經)"
        else: # sleepy
            # suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠ㅎㅎ"
            suggestionText = "졸린 당신을 위해 준비했습니다.\n귀엽게 들어주세요 :)"
        suggestionBox.setText(suggestionText)
        suggestionBox.setStyleSheet("QTextEdit {background-color: rgb(241, 241, 241); border-radius: 10px; padding: 10px;}")
        # suggestionBox.setAlignment(Qt.AlignVCenter)
        suggestionBox.setGeometry(90, 195, 250, 130)
        suggestionBox.setReadOnly(True)
        self.suggestionBox = suggestionBox
        suggestionBox.show()

        # 음악 재생 버튼
        self.play_btn = QPushButton(self)
        play_icon = QtGui.QIcon('./tab1_photo/play.png')
        self.play_btn.setIcon(play_icon)
        self.play_btn.setIconSize(QSize(30, 30))
        self.play_btn.setGeometry(105, 265, 30, 30)
        self.play_btn.setStyleSheet("{background-color: rgb(241, 241, 241);}")
        self.play_btn.clicked.connect(lambda: self.music_play("play")) # 재생
        self.play_btn.show()

        # 음악 멈춤 버튼
        # self.stop_btn = QPushButton(self)
        # stop_icon = QtGui.QIcon('./tab1_photo/pause.png')
        # self.stop_btn.setIcon(stop_icon)
        # self.stop_btn.setIconSize(QSize(30, 30))
        # self.stop_btn.setGeometry(105, 265, 30, 30)
        # self.stop_btn.setStyleSheet("{background-color: rgba(241, 241, 241);}")
        # self.stop_btn.clicked.connect(lambda: self.music_play("pause")) # 멈춤
        # self.stop_btn.hide()

        # Music wave
        try:
            movie = QMovie('./tab1_photo/wave.gif')  # , QByteArray(), self
            movie.setScaledSize(QSize(150, 100))
            music_label = QLabel(self)
            music_label.setMovie(movie)
            music_label.show()
            music_label.setGeometry(150, 250, 150, 60)
            self.movie = movie
            movie.start()
            movie.loopCount()
        except Exception as e:
            print(e)

        # Music player
        self.musicThread = MusicPlay(self.emotion)

    def add_response_box(self):
        def okay():
            responseBox.hide()
            okayButton.hide()
            refreshButton.hide()

            responseBox2 = QTextEdit(self)
            responseBox2.setText("마음에 들어!")
            responseBox2.setStyleSheet("QTextEdit {background-color: rgb(6, 136, 255); border-radius: 10px; padding: 10px; color: rgb(255, 255, 255)}")
            responseBox2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            responseBox2.setGeometry(275, 363, 250, 42)
            responseBox2.setReadOnly(True)
            self.responseBox = responseBox2
            responseBox2.show()

        def refresh():
            # self.catLabel2.hide()
            # self.suggestionBox.hide()
            # self.play_btn.hide()
            # self.movie.hide()
            #
            # self.faceLabel2.hide()
            # self.responseBox.hide()
            # self.okayButton.hide()
            # self.refreshButton.hide()
            # 더 음악이 추가되면 그런 것들도 hide해야 함.
            self.add_suggestion_box()
            # self.add_response_box()

        faceLabel = QLabel(self)
        faceLabel.setPixmap(self.getPixmap(""))
        faceLabel.setGeometry(539, 349, 56, 56)
        self.faceLabel2 = faceLabel
        faceLabel.show()

        responseBox = QTextEdit(self)
        responseBox.setStyleSheet("QTextEdit {background-color: rgb(6, 136, 255); border-radius: 10px; padding: 10px;}")
        responseBox.setGeometry(275, 363, 250, 42)
        responseBox.setReadOnly(True)
        self.responseBox = responseBox
        responseBox.show()

        okayButton = QPushButton('좋아', self)
        okayButton.setStyleSheet("QPushButton {background-color: rgb(6, 136, 255); color: rgb(255, 255, 255);}")
        okayButton.setGeometry(290, 374, 30, 20)
        okayButton.clicked.connect(okay)
        self.okayButton = okayButton
        okayButton.show()

        refreshButton = QPushButton('다른 노래 추천해줘', self)
        refreshButton.setStyleSheet("QPushButton {background-color: rgb(6, 136, 255); color: rgb(255, 255, 255);}")
        refreshButton.setGeometry(400, 374, 110, 20)
        refreshButton.clicked.connect(refresh)
        self.refreshButton = refreshButton
        refreshButton.show()

    def music_play(self, part):
        if part == "play":
            self.musicThread.play()
            # self.play_btn.hide()
            # self.stop_btn.show()
        else:  # part == "pause"
            self.musicTread.pause()
            self.stop_btn.hide()
            self.play_btn.show()

class MusicPlay():
    def __init__(self, emotion):
        # super(MusicPlay, self).__init__(parent)
        path = "./media/" + emotion + "/"
        music_list = os.listdir(path)
        music_name = music_list.pop(random.randrange(len(music_list)))
        music_file = path + music_name

        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(1)

        try:
            pygame.mixer.music.load(music_file)
            print(" %s 로드" % music_file)
        except pygame.error:
            print(" %s 에러 (%s)" % (music_file, pygame.get_error()))

    def play(self):
        pygame.mixer.music.play()

    # def pause(self):
    #     pygame.mixer.music.stop()
    #     # pygame.mixer.music.pause()