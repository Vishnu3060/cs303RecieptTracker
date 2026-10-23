# pyqt6 User Interface for cs303 Reciept Tracker
# requires main.ui, items.ui, and camera.ui and installing pyqt6 by running "pip install pyqt6"
# Author Joey Staebler

import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QMainWindow, QDialog
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # fetch main window UI and set its window title
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Reciept Scanner")

        # button actions
        self.quitButton.clicked.connect(self.quit)
        self.scanButton.clicked.connect(self.openScanner)
        self.listButton.clicked.connect(self.openItems)
        self.actionQuit.triggered.connect(self.quit)

    # pressed quit button action
    def quit(self):
        sys.exit()

    # pressed scan button action
    def openScanner(self):
        self.scanWindow = CameraDialog()
        self.scanWindow.show()

    # pressed item list button action
    def openItems(self):
        self.itemWindow = ItemDialog()
        self.itemWindow.show()


class ItemDialog(QWidget):
    def __init__(self):
        super().__init__()

        # fetch item UI and set window title
        uic.loadUi('items.ui', self)
        self.setWindowTitle("My Items")

        # button actions
        self.backButton.clicked.connect(self.goBack)
        self.scanButton.clicked.connect(self.openScanner)

    # pressed back button (for now close the window will imporve later)
    def goBack(self):
        self.close()

    # pressed scan button action
    def openScanner(self):
        self.scanWindow = CameraDialog()
        self.scanWindow.show()

class CameraDialog(QDialog):
    def __init__(self):
        super().__init__()

        # fetch camera UI and set window title
        uic.loadUi('camera.ui', self)
        self.setWindowTitle("Scan Reciept")

        # button actions
        self.backButton.clicked.connect(self.goBack)

    # pressed back button (for now close the window will imporve later)
    def goBack(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # window instence
    window = MainWindow()
    window.show()

    app.exec()