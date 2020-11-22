import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import uic


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        uic.loadUi('main.ui', self)
        self.cur = sqlite3.connect('coffee.db').cursor()
        self.loadtable()

    def loadtable(self):
        res = self.cur.execute('SELECT * FROM coffee_table').fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(7)
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
