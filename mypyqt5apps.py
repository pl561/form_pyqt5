#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from pomodoro import Pomodoro
from systemtraymenubar import MySystemTray



def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    w = Pomodoro()

    tray = MySystemTray()
    menu = tray.get_menu()
    timer_action = menu.addAction("Timer")
    timer_action.triggered.connect(w.show)

    app.exec_()


if __name__ == '__main__':
    sys.exit(main())