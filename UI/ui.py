# pyqt6 User Interface for cs303 Reciept Tracker
# requires main.ui, items.ui, and camera.ui and installing pyqt6 by running "pip install pyqt6"
# Author Joey Staebler

import sys
import subprocess

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QDialogButtonBox, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QMainWindow, QDialog, QMessageBox, QTableWidgetItem
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
        self.receiptsButton.clicked.connect(self.openRecieptsWindow)
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

    def openRecieptsWindow(self):
        self.recieptsWindow = MyReceipts()
        self.recieptsWindow.show()

class AddItem(QWidget):
    def __init__(self):
        super().__init__()

        # fetch Additem window ui and set title
        uic.loadUi("additem.ui", self)
        self.setWindowTitle("Add Missing Item")

        # button actions
        ok_button = self.buttonBox.button(QDialogButtonBox.StandardButton.Ok)
        cancel_button = self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel)

        ok_button.clicked.connect(self.on_ok)
        cancel_button.clicked.connect(self.on_cancel)

    def on_ok(self):
        # add the item to the database
        name = self.text_item_name.toPlainText().strip().lower()
        price = int(self.text_price.toPlainText().strip())
        qty = int(self.text_qty.toPlainText().strip())
        category = self.text_category.toPlainText().strip()
        notes = self.text_notes.toPlainText()
        receipt_id = int(self.receipt_id.toPlainText().strip())

        database_connection = sqlite3.connect("ReceiptRadarDatabasetemp.db")
        cur = database_connection.cursor()


        # insert the new item into the list of products
        product_query = """
            INSERT INTO Products (Item_name, Price, Qty, Category, Notes) 
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (Item_name) DO UPDATE SET Qty = Qty + excluded.Qty
        """
        cur.execute(product_query, (name, price, qty, category, notes))


        # search for item id from item name
        cur.execute("SELECT item_id FROM Products WHERE Item_name = ?", (name,))
        row = cur.fetchone()
        item_id = row[0] if row else None



        # Check if this item is already on this receipt
        cur.execute("SELECT quanity FROM Receipt_item WHERE receipt_id = ? AND item_id = ?", (receipt_id, item_id))
        existing_item = cur.fetchone()

        if existing_item:
            cur.execute("UPDATE Receipt_item SET quanity = quanity + ? WHERE receipt_id = ? AND item_id = ?",(qty, receipt_id, item_id))
        else:
            cur.execute("INSERT INTO Receipt_item (receipt_id, item_id, name, price, quanity) VALUES (?, ?, ?, ?, ?)", (receipt_id, item_id, name, price, qty))

        # commit changes, close database, and close window
        database_connection.commit()
        database_connection.close()
        self.close()

    def on_cancel(self):
        self.close()

    


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
        self.addItemWindow = AddItem()
        self.addItemWindow.show()

    def editItems(self):
        pass


class MyReceipts(QDialog):
    def __init__(self):
        super().__init__()

        # fetch camera UI and set window title
        uic.loadUi('myreceipts.ui', self)

        self.loadTable()

        # button actions
        self.back_button.clicked.connect(self.goBack)


    def loadTable(self):
        # load database
        database_connection = sqlite3.connect("ReceiptRadarDatabasetemp.db")
        cur = database_connection.cursor()

        # get number of rows and ensure there are enough columns (if not force add missing columns)
        cur.execute("SELECT COUNT(*) FROM Receipts")
        row_count = cur.fetchone()[0] # get row count using fetchone() tuple (row,)
        self.receipt_table.setRowCount(row_count)
        self.receipt_table.setColumnCount(4)

        query = """
        SELECT
            Receipts.receipt_id,
            Receipts.date,
            Receipts.store_id,
            Stores.name,
            Stores.address
        FROM Receipts
        LEFT JOIN Stores ON Receipts.store_id = Stores.store_id
        """

        # load table widget from SQLlite database
        table_row = 0
        for row in cur.execute(query):
            self.receipt_table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.receipt_table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(str(row[3])))

            # format date with padding
            date_str = str(row[1]).zfill(8)
            formatted_date = f"{date_str[2:4]}/{date_str[:2]}/{date_str[4:]}"

            self.receipt_table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(formatted_date))
            self.receipt_table.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(row[4])))
            table_row += 1

        # close database
        database_connection.close()

    # pressed back button (for now close the window will imporve later)
    def goBack(self):
        self.close()



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





# IGNORE FOR NOW (error handling and subprocess testing)
        # exe_path = "./a.out"

        # try:
        #     testprocess = subprocess.run([exe_path], capture_output=True, text=True)
        # except Exception as e:
        #     QMessageBox.critical(self,"Error",f"Executable not found or failed to launch {str(e)}")

        # teststdout = testprocess.stdout.strip()

        # msgBox = QMessageBox(self)
        # msgBox.setWindowTitle("Warning")
        # msgBox.setText(teststdout)
        # msgBox.exec()

        # # temp hello world c++ stdout communication test
        # exe_path = "./a.out"

        # try:
        #     testprocess = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # except Exception as e:
        #     QMessageBox.critical(self,"Error",f"Executable not found or failed to launch {str(e)}")

        # teststdout = testprocess.stdout.strip()

        # msgBox = QMessageBox(self)
        # msgBox.setWindowTitle("Warning")
        # msgBox.setText(teststdout)
        # #msgBox.
        # msgBox.exec()