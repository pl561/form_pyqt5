#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

HOME = os.environ['HOME']


class AppExampleQWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.title = 'PyQt5 simple window with QWidget'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppExampleQWidget()
    sys.exit(app.exec_())
