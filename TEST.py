from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore

import multiprocessing

import webbrowser
import sys
import os
import shutil
import test_oauth
import uvicorn
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('testui.ui',self)

        self.pushButton.setText('open_url')
        self.pushButton_2.setText('print_responce')
        self.pushButton_4.setText('stop_srv')
        self.pushButton_3.setText('start_server')
        self.pushButton.clicked.connect(self.open_url)

    init_url = 'http://localhost:8000/authorize'
    
    def open_url(self):
        webbrowser.open(self.init_url)
    



def start_server():
    uvicorn.run("test_oauth:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == '__main__':
    proc = multiprocessing.Process(target=start_server, args=(), daemon=False)
    proc.start()

    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    statusbar = QtWidgets.QStatusBar()
    widget.addWidget(mainwindow)
    widget.setFixedSize(501,590)
    widget.show()
    sys.exit(app.exec_())






