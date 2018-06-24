#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os
import datetime

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, \
    QTextEdit, QLineEdit, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal


HOME = os.environ['HOME']


class MyTextEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(400, 400)
        self.nb_tabs = 0
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.t1 = QWidget()
        self.t2 = QWidget()

        self.add_tab()
        self.add_tab()

        # self.tabs.resize(600, 600)
        self.t1.layout = QVBoxLayout()
        qte = QTextEdit()
        self.t1.layout.addWidget(qte)
        self.t1.setLayout(self.t1.layout)

        button = QPushButton("Add tab")
        button.clicked.connect(self.add_tab)

        self.main_layout.addWidget(button)
        self.main_layout.addWidget(self.tabs)

        self.setLayout(self.main_layout)

    def close_tab(self, index):
        self.tabs.removeTab(index)

    def add_tab(self):
        self.nb_tabs += 1
        w = QWidget()
        tab_name = "Tab {}".format(self.nb_tabs)
        self.tabs.addTab(w, tab_name)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MyTextEditor()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())