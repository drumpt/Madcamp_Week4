import sys

# from PyQt5 import QtM
from PyQt5.QtWidgets import *

import start_1
import tab1
import tab2


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = start_1.StartDialog()
    Dialog = QDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
