#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os

from PyQt5 import QtWidgets, Qt, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal

HOME = os.environ['HOME']

class TimerSignals(Qt.QObject):
    start = pyqtSignal()
    stop = pyqtSignal()
    toggle = pyqtSignal()

class SelectiveWidget(QtWidgets.QWidget):
    def __init__(self, mode="lcd", parent=None):
        super().__init__(parent=parent)
        self.mode = mode
        if self.mode == "lcd":
            self.widget = QtWidgets.QLCDNumber(parent=parent)
        elif self.mode == "lbl":
            self.widget = QtWidgets.QLabel(parent=parent)

class MyTimer(QtCore.QTimer):
    """amount in seconds
       by default timer is deactivated"""
    def __init__(self, amount, parent=None):
        super().__init__(parent=parent)
        self.setInterval(1000)
        self.amount = amount
        self.timeout(self.update)
        self.is_ticking = False
        # self.

    def toggle(self):
        if self.is_ticking:
            self.stop()
        else:
            self.start(1000)
        self.is_ticking = not self.is_ticking

    def update(self):
        if self.amount > 0:
            self.amount += -1
            self.is_ticking = True
        else:
            TimerSignals.toggle.emit()

class Timer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.title = "Timer"
        self.left, self.top = 10, 10
        self.width, self.height = 300, 300
        self.init_ui()

    def init_it(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        central_widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(central_widget)

        self.timer = QtCore.QTimer()



def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Timer()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())