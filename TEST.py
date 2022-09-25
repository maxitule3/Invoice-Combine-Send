
import webbrowser
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import server
import sys
import os
import threading
import otest


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('testui.ui',self)

        self.pushButton_4.setText('print params')
        self.pushButton_3.setText('start_server')
        self.pushButton_2.setText('auth')

        self.pushButton_3.clicked.connect(self.strt_srv)
        self.pushButton_2.clicked.connect(self.start_flow)

    
    def strt_srv(self):
        srv_thread = threading.Thread(target=server.start_srv, daemon=True)
        srv_thread.start()

    def start_flow(self):
        otest.authorize()


    




app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
statusbar = QtWidgets.QStatusBar()
widget.addWidget(mainwindow)
widget.setFixedSize(501,590)
widget.show()
sys.exit(app.exec_())






