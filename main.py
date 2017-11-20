#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton,\
    QGridLayout, QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit, QMenu, QMenuBar
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import numpy as np

HOME = os.environ['HOME']


class App(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.title = 'PyQt5 simple QMainWindow'
        self.left, self.top = 10, 10
        self.width, self.height = 600, 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.set_message("Hello")

        central_widget = QWidget(parent=self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(PyQt5.QtCore.Qt.AlignLeft)
        btn_test = QPushButton("test", parent=central_widget)
        btn_test.clicked.connect(self.activated_btn)
        btn_test.setAutoDefault(False)
        btn_test.setMaximumSize(btn_test.minimumSizeHint())

        btn2 = QtWidgets.QPushButton("test2", parent=central_widget)

        btn2.setMaximumSize(btn_test.sizeHint())
        # btn2.setAcceptDrops(True)


        main_layout.addWidget(btn_test)
        # main_layout.addWidget(btn2)

        central_widget.setLayout(main_layout)






    def set_message(self, msg):
        self.statusBar().showMessage(str(msg))

    @pyqtSlot()
    def activated_btn(self):
        self.set_message("random number = {}".format(np.random.rand()))
        answer =  QtWidgets.QMessageBox
        choices = answer.Yes | answer.No | answer.Cancel
        btn_question = QtWidgets.QMessageBox.question(self, "Question box",
                                                      "Do you like PyQt5 ?",
                                                      choices, answer.Cancel)
        if btn_question == answer.Yes:
            self.set_message("YES")
        elif btn_question == answer.No:
            self.set_message("NO")
        else:
            self.set_message("Cancelled")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
