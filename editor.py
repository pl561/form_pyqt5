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


class MyQTextEdit(QtWidgets.QTextEdit):
    # todo : if file has changed on disk, what do we do ?
    def __init__(self, basename, directory="notes", parent=None):
        super().__init__(parent=parent)

        basepath = os.path.dirname(os.path.abspath(__file__))
        notes_dir = os.path.join(basepath, directory)
        if not os.path.exists(notes_dir):
            os.mkdir(notes_dir)

        self.content_fname = os.path.join(basepath, directory, basename)
        print(self.content_fname)
        self.current_content = ""
        if os.path.exists(self.content_fname):
            self.read_content()
        else:
            self.save_content(force_write=True)
        self.init_ui()

    def init_ui(self):
        self.init_timer()

    def init_timer(self):
        self.n = 1000 * 5
        self.ticker = QtCore.QTimer()
        self.ticker.timeout.connect(self.save_content)
        self.ticker.setInterval(self.n)
        self.ticker.start(self.n)

    def save_content(self, force_write=False):
        new_content = str(self.toPlainText())
        if new_content != self.current_content or force_write:
            print(str(datetime.datetime.now())+" write")
            self.current_content = new_content
            with open(self.content_fname, "w") as fd:
                fd.write(new_content)

    def read_content(self):
        with open(self.content_fname, "r") as fd:
            content = fd.read()
        self.current_content = content
        self.setPlainText(content)



class MyTextEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(400, 400)
        self.nb_tabs = 0
        self.tab_dict = {}
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        # self.tabs.setTabsClosable(True)
        # self.tabs.tabCloseRequested.connect(self.close_tab)

        self.open_note("now")
        self.open_note("done")
        self.open_note("log")
        self.open_note("tips")

        # self.tabs.resize(600, 600)
        # self.t1.layout = QVBoxLayout()
        # qte = QTextEdit()
        # self.t1.layout.addWidget(qte)
        # self.t1.setLayout(self.t1.layout)

        # button = QPushButton("Add tab")
        # button.clicked.connect(self.add_tab)

        # self.main_layout.addWidget(button)
        self.main_layout.addWidget(self.tabs)

        self.setLayout(self.main_layout)


    def open_note(self, fname):
        tab = MyQTextEdit(fname)
        self.tab_dict[fname] = tab
        self.tabs.addTab(tab, fname)

    def close_tab(self, index):
        self.tabs.removeTab(index)

    # def add_tab(self):
    #     self.nb_tabs += 1
    #     w = QWidget()
    #     tab_name = "Tab {}".format(self.nb_tabs)
    #     self.tabs.addTab(w, tab_name)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MyTextEditor()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())