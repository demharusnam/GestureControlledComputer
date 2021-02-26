
import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel, QRadioButton,
                             QPlainTextEdit, QWidget, QGridLayout)
from PyQt5.QtCore import QSize, QThread, QObject
from PyQt5.Qt import (QApplication, QClipboard)


class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: Grey;")
        self.setWindowTitle("Controls")
        self.setGeometry(0, 0, 2160, 1920)

        self.titlecontrol = QLabel('Controls', self)
        self.titlecontrol.setFont(QFont('Arial', 30))
        self.titlecontrol.move(900, -75)
        self.titlecontrol.resize(400, 200)

        self.fist = QPixmap('cursor.png')
        self.fistlabel = QLabel(self)
        self.fistlabel.setPixmap(self.fist)
        self.fistlabel.move(0, 100)
        self.fistlabel.resize(200, 300)

        self.cursorinfo = QLabel('Control 1: Cursor', self)
        self.cursorinfo.setFont(QFont('Calibri', 20))
        self.cursorinfo.move(210, 20)
        self.cursorinfo.resize(400, 200)

        self.cursorinfo2 = QLabel('Make a fist to control the cursor', self)
        self.cursorinfo2.setFont(QFont('Calibri', 14))
        self.cursorinfo2.move(210, 150)
        self.cursorinfo2.resize(400, 50)

        self.leftclick = QPixmap('leftclick.png')
        self.leftclicklabel = QLabel(self)
        self.leftclicklabel.setPixmap(self.leftclick)
        self.leftclicklabel.move(0, 500)
        self.leftclicklabel.resize(233, 170)

        self.leftinfo = QLabel('Control 2: Left Click', self)
        self.leftinfo.setFont(QFont('Calibri', 20))
        self.leftinfo.move(243, 410)
        self.leftinfo.resize(400, 200)

        self.leftinfo2 = QLabel('Make a fist and extend the thumb to left click', self)
        self.leftinfo2.setFont(QFont('Calibri', 14))
        self.leftinfo2.move(243, 540)
        self.leftinfo2.resize(520, 50)

        self.rightclick = QPixmap('rightclick.png')
        self.rightclicklabel = QLabel(self)
        self.rightclicklabel.setPixmap(self.rightclick)
        self.rightclicklabel.move(0, 750)
        self.rightclicklabel.resize(203, 203)

        self.rightinfo = QLabel('Control 3: Right Click', self)
        self.rightinfo.setFont(QFont('Calibri', 20))
        self.rightinfo.move(213, 720)
        self.rightinfo.resize(400, 100)

        self.rightinfo2 = QLabel('Make a fist and extend the thumb & index finger to right click', self)
        self.rightinfo2.setFont(QFont('Calibri', 14))
        self.rightinfo2.move(213, 800)
        self.rightinfo2.resize(715, 50)

        self.drag = QPixmap('drag.png')
        self.draglabel = QLabel(self)
        self.draglabel.setPixmap(self.drag)
        self.draglabel.move(1000, 100)
        self.draglabel.resize(127, 185)

        self.draginfo = QLabel('Control 4: Drag', self)
        self.draginfo.setFont(QFont('Calibri', 20))
        self.draginfo.move(1137, 70)
        self.draginfo.resize(400, 100)

        self.draginfo2 = QLabel('Point the index & middle finger up to click and drag', self)
        self.draginfo2.setFont(QFont('Calibri', 14))
        self.draginfo2.move(1137, 150)
        self.draginfo2.resize(715, 50)

        self.doubleclick = QPixmap('doubleclick.png')
        self.doublelabel = QLabel(self)
        self.doublelabel.setPixmap(self.doubleclick)
        self.doublelabel.move(1000, 400)
        self.doublelabel.resize(136, 194)

        self.doubleinfo = QLabel('Control 5: Double Click', self)
        self.doubleinfo.setFont(QFont('Calibri', 20))
        self.doubleinfo.move(1146, 370)
        self.doubleinfo.resize(400, 100)

        self.doubleinfo2 = QLabel('Point the index, middle finger, & thumb up to double click', self)
        self.doubleinfo2.setFont(QFont('Calibri', 14))
        self.doubleinfo2.move(1146, 440)
        self.doubleinfo2.resize(715, 50)


class Window3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: Grey;")
        self.setWindowTitle("Options")
        self.setGeometry(600, 200, 600, 600)

        self.settingD = QRadioButton("Choice 1", self)
        self.settingD.move(50, 200)

        self.settingE = QRadioButton("Choice 2", self)
        self.settingE.move(200, 200)

        self.settingF = QRadioButton("Choice 3", self)
        self.settingF.move(350, 200)

        self.settingAButton = QPushButton("Option 1", self)
        self.settingAButton.move(50, 50)

        self.settingBButton = QPushButton("Option 2", self)
        self.settingBButton.move(50, 100)

        self.settingBButton = QPushButton("Option 3", self)
        self.settingBButton.move(50, 150)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Gesture Control App v0.2", self)
        self.title = "Gesture Control Main Menu"
        self.top = 600
        self.left = 200
        self.width = 600
        self.height = 600

        self.gestureStartButton = QPushButton("Start", self)
        self.gestureStartButton.move(250, 350)
        self.gestureStartButton.clicked.connect(self.startclick)

        self.gestureStopButton = QPushButton("Stop", self)
        self.gestureStopButton.move(250, 400)
        self.gestureStopButton.clicked.connect(self.stopclick)

        self.controlButton = QPushButton("Controls", self)
        self.controlButton.move(250, 450)
        self.controlButton.clicked.connect(self.window2)  # <===

        self.optionsButton = QPushButton("Options", self)
        self.optionsButton.move(250, 500)
        self.optionsButton.clicked.connect(self.window3)

        self.main_window()

    def stopclick(self):
        print("The gesture control has been stopped")

    def startclick(self):
        print("The gesture control is now running")

    def main_window(self):
        self.setStyleSheet("background-color: Turquoise;")
        self.label.setFont(QFont('Arial', 24))
        self.label.resize(600, 300)
        self.label.move(30, -100)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def window2(self):
        self.w = Window2()
        self.w.show()
        # self.hide()

    def window3(self):  # <===
        self.w = Window3()
        self.w.show()
        # self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
