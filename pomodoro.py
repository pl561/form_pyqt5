#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os

from PyQt5 import QtWidgets, Qt, QtGui, QtCore
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import pyqtSignal

HOME = os.environ['HOME']

class MyTimer(QtCore.QTimer):
    """customized timer
       amount in seconds
       by default timer is deactivated"""
    start_signal = pyqtSignal(str)
    tick_signal = pyqtSignal(int)
    stop_signal = pyqtSignal(str)
    def __init__(self, amount, sound_fname="", parent=None):
        super().__init__(parent=parent)
        self.setInterval(1000)
        self.set_amount(amount)
        self.timeout.connect(self.update)
        self.is_ticking = False
        self.sound_obj = QSound(sound_fname, parent=self)

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

    def toggle(self):
        if self.is_ticking:
            self.stop_ticking()
        else:
            self.start_ticking()

    def update(self):
        if self.amount > 0:
            self.amount += -1
            self.tick_signal.emit(self.get_amount())
        else:
            self.stop_ticking()
            self.sound_obj.play()

    def start_ticking(self):
        self.start(1000)
        self.start_signal.emit("started")
        self.is_ticking = True

    def stop_ticking(self):
        self.stop()
        self.stop_signal.emit("stopped")
        self.is_ticking = False


class MyLCDNumber(QtWidgets.QLCDNumber):
    click_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def display_time(self, amount):
        minutes = str(amount//60).zfill(2)
        seconds = str(amount%60).zfill(2)
        content = "{}:{}".format(minutes, seconds)
        self.display(content)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.click_signal.emit()
        else:
            super().mousePressEvent(event)


class Pomodoro(QtWidgets.QMainWindow):
    """main window containing the timer widget
       duration in minutes"""
    def __init__(self, duration, sound_fname="", parent=None):
        super().__init__(parent=parent)
        self.title = "Pomodoro Timer"
        self.left, self.top = 10, 10
        self.width, self.height = 200, 150
        self.duration = duration
        self.sound_fname = sound_fname
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage("Click on LCD to start the timer.")
        central_widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)
        # layout.setAlignment(QtCore.Qt.AlignTop)
        self.display_widget = MyLCDNumber(parent=central_widget)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal,
                                        parent=central_widget)
        self.slider.setMinimum(0)
        self.slider.setMaximum(60)
        self.slider.setValue(self.duration)
        self.slider.setTickInterval(5)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)

        self.timer = MyTimer(self.duration, self.sound_fname)
        self.timer.tick_signal.connect(self.display_widget.display_time)
        self.timer.start_signal.connect(self.show_message)
        self.timer.stop_signal.connect(self.show_message)

        self.update_slider_change(self.duration)
        self.slider.valueChanged.connect(self.update_slider_change)

        # when the LCD widget captures a click, toggle timer and status
        self.display_widget.click_signal.connect(self.timer.toggle)

        layout.addWidget(self.display_widget)
        layout.addWidget(self.slider)

    def update_slider_change(self, amount):
        self.timer.set_amount(amount*60)
        self.display_widget.display_time(amount*60)

    def show_message(self, msg):
        self.statusBar().showMessage(msg)

    def show_stop_message(self):
        self.show_message("Stopped")


def main():
    app = QtWidgets.QApplication(sys.argv)
    sound_fname = "/home/lefevre/phd_git/sounds/sms-alert-4-daniel_simon.wav"
    minutes = 25
    ex = Pomodoro(minutes, sound_fname)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())