# pyqt6 User Interface for cs303 Reciept Tracker
# requires main.ui, items.ui, and camera.ui and installing pyqt6 by running "pip install pyqt6"
# Author Joey Staebler

import sys
import subprocess

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QMainWindow, QDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import uic
import sqlite3

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

        # load database
        database_connection = sqlite3.connect("ReceiptRadarDatabasetemp.db")
        cur = database_connection.cursor()

        # get number of rows and ensure there are enough columns (if not force add missing columns)
        cur.execute("SELECT COUNT(*) FROM Products")
        row_count = cur.fetchone()[0] # get row count using fetchone() tuple (row,)
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(5)

        query = """
        SELECT
            Products.item_id,
            Products.Item_name,
            Products.Price,
            Products.Qty,
            Products.Category
        FROM Products
        """

        # load table widget from SQLlite database
        table_row = 0
        for row in cur.execute(query):
            self.tableWidget.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(table_row, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.tableWidget.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(table_row, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            table_row += 1

        # close database
        database_connection.close()


        # button actions
        self.backButton.clicked.connect(self.goBack)
        self.scanButton.clicked.connect(self.openScanner)
        self.addItemButton.clicked.connect(self.addItemAction)
        self.editButton.clicked.connect(self.editItems)

    # pressed back button (for now close the window will imporve later)
    def goBack(self):
        self.close()

    # pressed scan button action
    def openScanner(self):
        self.scanWindow = CameraDialog()
        self.scanWindow.show()

    def addItemAction(self):
        # temp hello world c++ stdout communication test
        exe_path = "./a.out"

        try:
            testprocess = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            QMessageBox.critical(self,"Error",f"Executable not found or failed to launch {str(e)}")

        teststdout = testprocess.stdout.strip()

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Warning")
        msgBox.setText(teststdout)
        #msgBox.
        msgBox.exec()

    def editItems(self):
        exe_path = "./a.out"

        try:
            testprocess = subprocess.run([exe_path], capture_output=True, text=True)
        except Exception as e:
            QMessageBox.critical(self,"Error",f"Executable not found or failed to launch {str(e)}")

        teststdout = testprocess.stdout.strip()

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Warning")
        msgBox.setText(teststdout)
        msgBox.exec()




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