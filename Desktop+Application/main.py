"""import sys
from PyQt5 import QtWidgets, QtCore

# This is a sample Python script.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.resize(700, 700)
widget.setWindowTitle("Gesture Control")
widget.show()
exit(app.exec_())
"""
import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel, QRadioButton,
                             QPlainTextEdit)
from PyQt5.QtCore import QSize
from PyQt5.Qt import (QApplication, QClipboard)


class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: Grey;")
        self.setWindowTitle("Controls")
        self.setGeometry(600, 200, 600, 600)

        self.written = QLabel('These are the controls', self)
        self.written.setFont(QFont('Arial', 16))
        self.written.move(130, -80)
        self.written.resize(400, 200)


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

        self.label = QLabel("Gesture Control App v0.1", self)
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
