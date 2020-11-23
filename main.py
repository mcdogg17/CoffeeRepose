import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QDialog
from main_ui import Ui_Form
from addEditCoffeeForm import Ui_Dialog


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.setupUi(self)
        self.cur = sqlite3.connect('data/coffee.db').cursor()
        self.changeedit.clicked.connect(self.changeEdit)
        self.loadtable()

    def loadtable(self):
        self.res = self.cur.execute('SELECT * FROM coffee_table').fetchall()
        self.tableWidget.setRowCount(len(self.res))
        self.tableWidget.setColumnCount(7)
        for i, elem in enumerate(self.res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def changeEdit(self):
        add = addEditCoffee()
        add.exec()


class addEditCoffee(QDialog, Ui_Dialog):
    def __init__(self):
        super(addEditCoffee, self).__init__()
        self.setupUi(self)
        self.add.clicked.connect(self.addCoffee)
        self.cur = sqlite3.connect('data/coffee.db').cursor()
        self.res = self.cur.execute('SELECT * FROM coffee_table').fetchall()

        for i in self.res:
            if i[0] == 1:
                self.currentIndex = i[0]
                self.deg_2.setText(i[2])
                self.ground_2.setCurrentText(i[3])
                self.descrip_2.setText(i[4])
                self.price_2.setValue(i[5])
                self.volume_2.setValue(i[6])
            self.name_2.addItem(i[1])

        self.name_2.currentTextChanged.connect(self.currentCoffee)
        self.change.clicked.connect(self.changeCoffee)

    def addCoffee(self):
        self.cur.execute('INSERT INTO coffee_table VALUES'
                         ' (?, ?, ?, ?, ?, ?, ?)',
                         (None, self.name.text(), self.deg.text(),
                          self.ground.currentText(), self.descrip.text(),
                          self.price.value(), self.volume.value()))
        self.cur.connection.commit()
        self.close()
        ex.loadtable()

    def currentCoffee(self):
        for i in self.res:
            if i[1] == self.name_2.currentText():
                self.currentIndex = i[0]
                self.deg_2.setText(i[2])
                self.ground_2.setCurrentText(i[3])
                self.descrip_2.setText(i[4])
                self.price_2.setValue(i[5])
                self.volume_2.setValue(i[6])
                break

    def changeCoffee(self):
        self.cur.execute(f'UPDATE coffee_table SET deg = ?'
                         f' WHERE ID = ?', (self.deg_2.text(), self.currentIndex))
        self.cur.execute(f'UPDATE coffee_table SET ground = ? '
                         f'WHERE ID = ?', (self.ground_2.currentText(), self.currentIndex))
        self.cur.execute(f'UPDATE coffee_table SET descrip = ? '
                         f'WHERE ID = ?', (self.descrip_2.text(), self.currentIndex))
        self.cur.execute(f'UPDATE coffee_table SET price == ? '
                         f'WHERE ID = ?', (self.price_2.value(), self.currentIndex))
        self.cur.execute(f'UPDATE coffee_table SET volume = ? '
                         f'WHERE ID = ?', (self.volume_2.value(), self.currentIndex))
        self.cur.connection.commit()
        ex.loadtable()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
