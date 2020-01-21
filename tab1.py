import os
import random
import time

import cv2
import pygame
from PyQt5 import QtGui
from PyQt5.QtCore import *
# from PyQt5 import QtM
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tensorflow.keras.models import load_model

# import my_magenta

# for face detection
face_cascade = cv2.CascadeClassifier("C:/Users/q/Downloads/haarcascade_frontalface_alt.xml")
eye_cascade = cv2.CascadeClassifier("C:/Users/q/Downloads/haarcascade_eye_tree_eyeglasses.xml")
model = load_model("C:/Users/q/Downloads/another_model_2_10.h5", compile=False)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

ITERATION = 5

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
            # print(self.face)
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

        print("여기까지 됩니다ㅎㅎ")

        catLabel = QLabel(self)
        catLabel.setPixmap(self.getPixmap(self.img_path))
        catLabel.setGeometry(20, 20, 56, 56)
        self.catLabel1 = catLabel
        catLabel.show()

        print("여기까지 됩니다ㅎㅎ")

        initBox = QTextEdit(self)
        initBox.setText("안녕하세요. 오늘 하루는 어떠셨나요? 당신의 기분이 궁금해요!")
        initBox.setStyleSheet("QTextEdit {background-color: rgb(241, 241, 241); border-radius: 10px; padding: 10px;}")
        initBox.setAlignment(Qt.AlignVCenter)
        initBox.setGeometry(90, 20, 250, 56)
        # initBox.setGeometry(20, 20, 250, 56)
        initBox.setReadOnly(True)
        self.initBox = initBox
        initBox.show()

        self.cnt = 1

        print(self.cnt)

        nextButton = QPushButton(self)
        nextButton.setIcon(QtGui.QIcon('./tab1_photo/tab1_next.jpg'))
        nextButton.setIconSize(QSize(60, 60))
        nextButton.setGeometry(QRect(530, 20, 60, 60))
        nextButton.clicked.connect(self.tab1_next)
        self.nextButton = nextButton
        nextButton.show()

        print("여기까지 됩니다!")

        self.initVoice = VoicePlay("")
        # print('Hello, world! 1')
        self.initVoice.play()
        # print('Hello, world! 2')
        # self.initVoice.play()
        # print('Hello, world! 3')
        print("여기까지 됩니다~~~")


    def add_answer_box(self):
        class_to_emotion = {0: 'angry', 1: 'happy', 2: 'neutral', 3: 'sad', 4: 'surprise'}
        emotion_to_word = {"happy": "오늘 기뻤어.", "sad": "오늘 슬펐어.", "angry": "오늘 화났어.", "sleepy": "지금 졸려."}
        emotions = []

        self.initVoice.stop()

        print("Hi!")

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
                eyes = eye_cascade.detectMultiScale(frame[y:y + h, x:x + w], scaleFactor=1.1, minNeighbors=5,
                                                    minSize=(20, 20))
                if len(eyes) == 0:
                    emotions.append("sleepy")
                    cnt += 1
                    if cnt == ITERATION - 2:
                        self.face = frame[y:y + h, x: x + w]
                else:
                    resized_face = cv2.cvtColor(cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY),
                                                cv2.COLOR_GRAY2BGR)
                    resized_frame = cv2.resize(resized_face, dsize=(48, 48), interpolation=cv2.INTER_AREA)
                    emotion = class_to_emotion[model.predict_classes(resized_frame.reshape([-1, 48, 48, 3]))[0]]
                    if emotion in ["happy", "sad", "angry"]:
                        emotions.append(emotion)
                        cnt += 1
                        if cnt == ITERATION - 2:
                            self.face = frame[y:y + h, x: x + w]
                print(cnt)
                # cv2.putText(frame, emotion, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cv2.waitKey(100)

            # Display the resulting frame
            cv2.imshow('Face_to_emotion', frame)
            cv2.waitKey(1)

            if cnt >= ITERATION or cv2.waitKey(1) & 0xFF == ord('q'):
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

        print("으아아악")

        answerBox = QTextEdit(self)
        answerBox.setText("나는 " + emotion_to_word[emotion])
        answerBox.setStyleSheet(
            "QTextEdit {background-color: rgb(6, 136, 255); border-radius: 10px; padding: 10px; color: rgb(255, 255, 255)}")
        answerBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        answerBox.setGeometry(275, 114, 250, 42)
        # answerBox.setGeometry(275, 100, 250, 42)
        answerBox.setReadOnly(True)

        # print("나는 " + emotion_to_word[emotion])

        self.answerBox = answerBox
        print("으아아악아아아악")
        answerBox.show()
        print("으아아악아아아악으억")

        self.cnt = 2

    def add_suggestion_box(self):
        emotion_to_word2 = {"happy": "기쁠", "sad": "슬플", "angry": "화날", "sleepy": "졸릴"}

        print("HI!!!!!!!!!!!!!!!")

        catLabel = QLabel(self)
        catLabel.setPixmap(self.getPixmap(self.img_path))
        catLabel.setGeometry(20, 195, 56, 56)
        self.catLabel2 = catLabel
        catLabel.show()

        print("Hello!!!!!!!!!!!!!!!")

        suggestionBox = QTextEdit(self)
        if self.emotion in ["happy", "sad"]:
            suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠!\n제가 직접 만들었어요ㅎㅎ"
            # if self.emotion == "happy":
            #     my_magenta.tab1_happy()
            # elif self.emotion == "sad":
            #     my_magenta.tab1_sad()
        elif self.emotion == "angry":
            # suggestionText = emotion_to_word2[self.emotion]
            suggestionText = "분노와 교만에 지배되지 말아라.\n그 뿌리를 뽑아 버려라 - 불경(佛經)"
        else:  # sleepy
            # suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠ㅎㅎ"
            suggestionText = "졸린 당신을 위해 준비했습니다.\n잘 들어주세요 :)"
        suggestionBox.setText(suggestionText)
        suggestionBox.setStyleSheet(
            "QTextEdit {background-color: rgb(241, 241, 241); border-radius: 10px; padding: 10px;}")
        # suggestionBox.setAlignment(Qt.AlignVCenter)
        suggestionBox.setGeometry(90, 195, 250, 130)
        suggestionBox.setReadOnly(True)
        self.suggestionBox = suggestionBox
        suggestionBox.show()

        print("Helloadgwp9y3r593015!!!!!!!!!!!!!!!")

        # 음악 재생 버튼
        self.play_btn = QPushButton(self)
        play_icon = QtGui.QIcon('./tab1_photo/play.png')
        self.play_btn.setIcon(play_icon)
        self.play_btn.setIconSize(QSize(30, 30))
        self.play_btn.setGeometry(105, 265, 30, 30)
        self.play_btn.setStyleSheet("{background-color: rgb(241, 241, 241);}")
        self.play_btn.clicked.connect(lambda: self.music_play("play"))  # 재생
        self.play_btn.show()

        # Music wave
        try:
            movie = QMovie('./tab1_photo/wave.gif')  # , QByteArray(), self
            movie.setScaledSize(QSize(150, 100))
            music_label = QLabel(self)
            music_label.setMovie(movie)
            music_label.show()
            music_label.setGeometry(150, 250, 150, 60)
            self.movie = movie
            self.movieLabel = music_label
            movie.start()
            movie.loopCount()
        except Exception as e:
            print(e)

        print("----------------.---------------")

        # Music player
        self.musicThread = MusicPlay(self.emotion)

        print(self.cnt)
        # time.sleep(1)
        # self.add_response_box()
        self.cnt = 3
        print(self.cnt)

        self.suggestionVoice = VoicePlay(self.emotion)
        self.suggestionVoice.play()

    def music_play(self, part):
        if part == "play":
            self.musicThread.play()
        else:  # part == "pause"
            self.musicTread.stop()

    def add_response_box(self):
        self.suggestionVoice.stop()

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
        okayButton.clicked.connect(self.okay)
        self.okayButton = okayButton
        okayButton.show()

        refreshButton = QPushButton('다른 노래 추천해줘', self)
        refreshButton.setStyleSheet("QPushButton {background-color: rgb(6, 136, 255); color: rgb(255, 255, 255);}")
        refreshButton.setGeometry(400, 374, 110, 20)
        refreshButton.clicked.connect(self.refresh)
        self.refreshButton = refreshButton
        refreshButton.show()
        self.cnt = 4

    def okay(self):
        self.suggestionVoice.stop()

        self.responseBox.hide()
        self.okayButton.hide()
        self.refreshButton.hide()

        responseBox2 = QTextEdit(self)
        responseBox2.setText("마음에 들어!")
        responseBox2.setStyleSheet(
            "QTextEdit {background-color: rgb(6, 136, 255); border-radius: 10px; padding: 10px; color: rgb(255, 255, 255)}")
        responseBox2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        responseBox2.setGeometry(275, 363, 250, 42)
        responseBox2.setReadOnly(True)
        self.responseBox = responseBox2
        responseBox2.show()

    def refresh(self):
        self.cnt = 2

        print("0")

        self.suggestionVoice.stop()

        print("a")

        self.catLabel2.hide()

        print("b")

        self.suggestionBox.hide()

        print("c")


        self.play_btn.hide()

        print("d")

        self.movieLabel.hide()

        print("e")

        # self.movie.deleteLater()
        # self.musicThread.stop()

        print("f")

        self.faceLabel2.hide()

        print("g")

        self.responseBox.hide()

        print("h")

        self.okayButton.hide()

        print("i")

        self.refreshButton.hide()
        print("j")

        # self.refreshButton.close()

        # print("k")
        # self.add_suggestion_box()

    def restart(self):
        print("0")
        #
        # # self.initVoice.stop()
        # # self.suggestionVoice.stop()
        # # self.musicThread.stop()
        # pygame.mixer.music.stop()

        print("1")

        self.catLabel1.hide()

        print("2")

        self.initBox.hide()

        print("3")

        self.faceLabel1.hide()

        print("4")

        self.answerBox.hide()

        print("5")

        self.catLabel2.hide()

        print("6")

        self.suggestionBox.hide()


        print("7")

        self.play_btn.hide()

        print("8")

        self.movieLabel.hide()
        # self.movie.deleteLater()
        print("9")

        self.faceLabel2.hide()

        print("10")

        self.responseBox.hide()

        print("11")

        self.okayButton.hide()

        print("12")

        self.refreshButton.hide()
        # self.refreshButton.deleteLater()
        # self.refreshButton = None
        # self.refreshButton.setParent(None)

        print("13")
        #
        self.cnt = 1
        self.add_init_box(self.img_path)


    def tab1_next(self):
        print(self.cnt)
        if self.cnt == 0:
            self.add_init_box(self.img_path)
        elif self.cnt == 1:
            self.add_answer_box()
        elif self.cnt == 2:
            self.add_suggestion_box()
        elif self.cnt == 3:
            self.add_response_box()
        elif self.cnt == 4:
            print("Hi!")
            self.restart()
            # self.refresh()
            # print(str(self.cnt) + "하하")


class MusicPlay():
    def __init__(self, emotion):

        print(1)
        # super(MusicPlay, self).__init__(parent)
        path = "./media/" + emotion + "/"
        music_list = os.listdir(path)
        music_name = music_list.pop(random.randrange(len(music_list)))
        music_file = path + music_name

        self.music_file = music_file

    def play(self):
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        self.player = pygame.mixer
        self.player.init(freq, bitsize, channels, buffer)
        self.player.music.set_volume(1)

        try:
            print(3)
            self.player.music.load(self.music_file)
            print(" %s 로드" % self.music_file)
        except pygame.error:
            print(" %s 에러 (%s)" % (self.music_file, pygame.get_error()))

        # # self.player.find_channel(True).play(self.music_file)
        # self.player.Sound(self.music_file).play(1)
        # # self.player.Channel(0).play(self.music_file, 1)
        self.player.music.play(1)

    def stop(self):
        # self.player.Sound(self.music_file).stop()
        # self.player.Channel(0).stop()
        self.player.music.stop()

class VoicePlay():
    def __init__(self, emotion):
        if emotion == "":
            path = "./media/electric_voice/"
            music_name = "init_sound.mp3"
            music_file = path + music_name
        else:
            path = "./media/electric_voice/"
            music_name = "suggestion_" + emotion + ".mp3"
            music_file = path + music_name

        self.music_file = music_file

    def play(self):
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
        # self.player.Sound(self.music_file).play(1)
        # self.player.find_channel(True).play(self.music_file)
        # self.player.Channel(1).play(self.music_file, 1)
        # self.player.music.play(1)
        pygame.mixer.music.play(1)

    def stop(self):
        # self.player.Channel(1).stop()
        # self.player.Sound(self.music_file).stop()
        pygame.mixer.music.stop()