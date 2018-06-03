#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os


from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication


HOME = os.environ['HOME']


class MySystemTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.icon = QtGui.QIcon("icon2.png")
        self.setIcon(self.icon)
        self.setVisible(True)

        self.init_ui()

    def init_ui(self):
        self.menu = QtWidgets.QMenu()

        about_action = self.menu.addAction("About")
        exit_action = self.menu.addAction("Exit")

        exit_action.triggered.connect(QtCore.QCoreApplication.exit)

        self.setContextMenu(self.menu)


    def get_menu(self):
        return self.menu

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    tray = MySystemTray()

    app.exec_()




if __name__ == '__main__':
    sys.exit(main())