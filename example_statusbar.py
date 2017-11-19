#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QIcon

class AppExampleQStatusBar(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 status bar example'
        self.left = 20
        self.top = 20
        self.width = 600
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('test message')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppExampleQStatusBar()
    sys.exit(app.exec_())