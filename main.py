import sys

import cv2
from PyQt5.QtCore import *
# from PyQt5 import QtM
from PyQt5.QtWidgets import *
from tensorflow.keras.models import load_model

# for face detection
face_cascade = cv2.CascadeClassifier("C:/Users/q/Downloads/haarcascade_frontalface_alt.xml")
eye_cascade = cv2.CascadeClassifier("C:/Users/q/Downloads/haarcascade_eye_tree_eyeglasses.xml")
model = load_model("C:/Users/q/Downloads/another_model_2_10.h5", compile = False)
model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i
    return num

class mainWindow(QWidget):
    def __init(self):
        super().__init()

    def init_window(self):
        self.setWindowTitle('Main window')
        self.setGeometry(600, 300, 640, 480)
        self.setStyleSheet("QWidget {background-color: white;}")

        self.tab1 = FirstTab()
        self.tab2 = SecondTab()

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


class FirstTab(QWidget):

    def __init(self):
        super().__init__()

    def add_init_box(self):
        # layout = QVBoxLayout()

        initBox = QTextEdit(self)
        initBox.setText("안녕하세요. 오늘 하루는 어떠셨나요? 당신의 기분이 궁금해요!")
        initBox.setStyleSheet("QTextEdit {background-color: rgb(241, 241, 241); border-radius: 10px; padding: 10px;}")
        initBox.setAlignment(Qt.AlignVCenter)
        initBox.setGeometry(20, 20, 250, 56)
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
                else:
                    resized_face = cv2.cvtColor(cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY),
                                                cv2.COLOR_GRAY2BGR)
                    resized_frame = cv2.resize(resized_face, dsize=(48, 48), interpolation=cv2.INTER_AREA)
                    emotion = class_to_emotion[model.predict_classes(resized_frame.reshape([-1, 48, 48, 3]))[0]]
                    if emotion in ["happy", "sad", "angry"]:
                        emotions.append(emotion)
                        cnt += 1
                print(cnt)
                # cv2.putText(frame, emotion, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cv2.waitKey(100)

            # Display the resulting frame
            cv2.imshow('Face_to_emotion', frame)
            cv2.waitKey(1)

            if cnt >= 15 or cv2.waitKey(1) & 0xFF == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                break

        # emotion : happy, sad, angry, sleepy
        emotion = most_frequent(emotions)
        self.emotion = emotion
        print(emotion)

        answerBox = QTextEdit(self)
        answerBox.setText("나는 " + emotion_to_word[emotion])
        answerBox.setStyleSheet("QTextEdit {background-color: rgb(6, 136, 255); border-radius: 10px; padding: 10px; color: rgb(255, 255, 255)}")
        answerBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        answerBox.setGeometry(340, 100, 250, 42)
        answerBox.setReadOnly(True)
        answerBox.show()

    def add_suggestion_box(self):
        emotion_to_word2 = {"happy": "기쁠", "sad": "슬플", "angry": "화날", "sleepy": "졸릴"}
        suggestionBox = QTextEdit(self)
        if self.emotion in ["happy", "sad"]:
            suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠ㅎㅎ 제가 직접 만들었어요!"
        elif self.emotion == "angry":
            suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠ㅎㅎ "
        else:
            suggestionText = emotion_to_word2[self.emotion] + " 때는 이 노래가 최고죠ㅎㅎ "
        suggestionBox.setText(suggestionText)

class SecondTab(QWidget):
    def __init(self):
        super().__init__()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.init_window()
    window.tab1.add_init_box()
    window.tab1.add_answer_box()
    sys.exit(app.exec_())