import sys
import os

# from PyQt5 import QtM
from PyQt5.QtWidgets import *

import start_1
import tab1
import tab2
import tab3
import tab4
# import my_magenta


class mainWindow(QWidget):
    def __init(self):
        super().__init()

    def init_window(self):
        self.setWindowTitle('다재다냥★♬')
        self.setGeometry(600, 300, 640, 480)
        self.setStyleSheet("QWidget {background-color: white; }")

        self.tab1 = tab1.FirstTab()
        self.tab2 = tab2.SecondTab()
        self.tab3 = tab3.ThirdTab()
        self.tab4 = tab4.FourthTab()

        tabwidget = QTabWidget()
        tabwidget.addTab(self.tab1, "노래 추천")
        tabwidget.addTab(self.tab2, "편곡")
        tabwidget.addTab(self.tab3, "그림")
        tabwidget.addTab(self.tab4, "짠")
        # tabwidget.setStyleSheet(
        #     "QTabBar::tab {width: 100px; height: 30px; border: 1px solid white; background-image: url(./tab1_photo/bgi.jpg); font-family: '배달의민족 주아'; font-size: 18px} \
        #     QTabBar::tab:selected{border: 1px solid white; background: rgb(255, 202, 62); font-family: '배달의민족 주아'; font-size: 18px;}"
        # )

        tabwidget.setStyleSheet(
            "QTabBar::tab {width: 100px; height: 30px; border: 1px solid lightgray; background: lightgray; font-family: '배달의민족 주아'; font-size: 18px} \
            QTabBar::tab:selected {border: 1px solid lightgray; background: white; font-family: '배달의민족 주아'; font-size: 18px; margin-bottom: -10px}"
        )

        vbox = QVBoxLayout()
        vbox.addWidget(tabwidget)

        self.setLayout(vbox)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # my_magenta 실행
    # exec('my_magenta')
    # os.system('python my_magenta.py')
    # print("돼?>")

    ui = start_1.StartDialog()
    Dialog = QDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
