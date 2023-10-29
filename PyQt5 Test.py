#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 09:40:57 2021

@author: williamhou
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(0, 0, 1000, 800)
        self.setWindowTitle("Detect Language")
        self.initUI()
        
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Enter Text:")
        self.label.move(50,50)
    
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Run")
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText("button pressed by you")
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
    
window()