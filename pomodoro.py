#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import os
import datetime

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


class ToggleButton(QtWidgets.QPushButton):
    toggle_signal = pyqtSignal()
    def __init__(self, symbols=['>>', '<<'], parent=None):
        """first symbol describes toggle is off, when clicked, toggle is on
        and replaces symbol"""
        super().__init__(parent=parent)
        self.is_on = False
        self.symbols = {
            False: symbols[0],
            True: symbols[1]
        }
        self.setText(self.symbols[0])

    def toggle_symbol(self):
        self.is_on = not self.is_on
        self.setText(self.symbols[self.is_on])

    def mousePressEvent(self, event):
        events = [QtCore.Qt.LeftButton, QtCore.Qt.RightButton]
        if event.button() in events:
            self.toggle_symbol()
            self.toggle_signal.emit()



class CounterButton(QtWidgets.QPushButton):
    def __init__(self, counter=0, parent=None):
        super().__init__(parent=parent)
        self.counter = counter
        self.setText(str(counter))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.counter += 1
        elif event.button() == QtCore.Qt.RightButton:
            self.counter -= 1
        else:
            super().mousePressEvent(event)
        self.setText(str(self.counter))

class MyLCDNumber(QtWidgets.QLCDNumber):
    left_clicked = pyqtSignal()
    right_clicked = pyqtSignal()
    middle_clicked = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def display_time(self, amount):
        minutes = str(amount//60).zfill(2)
        seconds = str(amount%60).zfill(2)
        content = "{}:{}".format(minutes, seconds)
        self.display(content)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_clicked.emit()
        elif event.button() == QtCore.Qt.RightButton:
            self.right_clicked.emit()
        elif event.button() == QtCore.Qt.MiddleButton:
            self.middle_clicked.emit()
        else:
            super().mousePressEvent(event)

    # def mouseDoubleClickEvent(self, event):
    # ## double click in conflict simple click
    #     print("double click")
    #     # if event.button() == QtCore.Qt.RightButton:
    #     self.doubleright_clicked.emit()
    #     # else:
    #     super().mouseDoubleClickEvent(event)


class MyQTextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        basename = "notes.txt"
        directory = os.path.dirname(os.path.abspath(__file__))
        self.content_fname = os.path.join(directory, basename)
        self.current_content = ""
        if os.path.exists(self.content_fname):
            self.read_content()
        self.init_ui()

    def init_ui(self):
        self.init_timer()

    def init_timer(self):
        self.n = 1000 * 2
        self.ticker = QtCore.QTimer()
        self.ticker.timeout.connect(self.save_content)
        self.ticker.setInterval(self.n)
        self.ticker.start(self.n)

    def save_content(self):
        new_content = str(self.toPlainText())
        if new_content != self.current_content:
            print(str(datetime.datetime.now())+" write")
            self.current_content = new_content
            with open(self.content_fname, "w") as fd:
                fd.write(new_content)

    def read_content(self):
        with open(self.content_fname, "r") as fd:
            content = fd.read()
        self.current_content = content
        self.setPlainText(content)


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

        basename = "pomodoro_value"
        directory = os.path.dirname(os.path.abspath(__file__))
        self.configfile_path = os.path.join(directory, basename)
        if not os.path.exists(self.configfile_path):
            with open(self.configfile_path, "w") as fd:
                fd.write("15")

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage("Click on LCD to start the timer.")
        central_widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(central_widget)
        # layout.setAlignment(QtCore.Qt.AlignTop)
        self.display_widget = MyLCDNumber(parent=central_widget)
        self.display_widget.setMinimumHeight(70)
        self.display_widget.setMinimumWidth(160)

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
        self.display_widget.left_clicked.connect(self.timer.toggle)
        self.display_widget.right_clicked.connect(self.reset_timer_fromfile)
        self.display_widget.middle_clicked.connect(self.reset_timer)

        self.btn_counter = CounterButton()
        self.btn_open_editor = ToggleButton()
        self.btn_open_editor.toggle_signal.connect(self.open_editor)
        hl = QtWidgets.QHBoxLayout()
        hl.addWidget(self.btn_counter)
        hl.addWidget(self.btn_open_editor)
        self.editor = MyQTextEdit()
        self.editor.setMinimumHeight(200)

        self.main_layout.addWidget(self.display_widget)
        self.main_layout.addWidget(self.slider)
        # layout.addWidget(self.btn_counter)
        self.main_layout.addLayout(hl)
        self.main_layout.addWidget(self.editor)

    def update_slider_change(self, amount):
        self.timer.set_amount(amount*60)
        self.display_widget.display_time(amount*60)

    def reset_timer(self):
        amount = self.slider.value()
        self.update_slider_change(amount)

    def reset_timer_fromfile(self):
        self.update_slider_change(self.readvalue_fromfile())

    def readvalue_fromfile(self):
        with open(self.configfile_path, "r") as fd:
            value = fd.read()

        try:
            value = int(value)
        except:
            value = 15

        if value > 99:
            value = 99
        elif value < 1:
            value = 1
        else:
            value = 15

        return value

    def open_editor(self):
        editor_h = self.editor.size().height()
        current_h = self.size().height()
        if self.btn_open_editor.is_on:
            self.editor.hide()
            self.setFixedHeight(current_h-editor_h)
        else:
            self.editor.show()
            self.setFixedHeight(current_h+editor_h)


    def show_message(self, msg):
        self.statusBar().showMessage(msg)

    def show_stop_message(self):
        self.show_message("Stopped")


def main():
    app = QtWidgets.QApplication(sys.argv)
    sound_fname = "/home/lefevre/phd_git/sounds/sms-alert-4-daniel_simon.wav"
    minutes = 15
    ex = Pomodoro(minutes, sound_fname)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())
