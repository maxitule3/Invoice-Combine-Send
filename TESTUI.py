
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import server
import sys
import threading
import otest
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('testui.ui',self)

        self.pushButton_4.setText('print params')
        self.pushButton_3.setText('start_flow')
        self.pushButton_2.setText('auth')
        self.pushButton.setText('api_call_test')
        self.pushButton_3.clicked.connect(self.start_flow)

        self.pushButton.clicked.connect(self.test_authorize)

    


    def start_flow(self):
        srv_thread = threading.Thread(target=server.start_srv, daemon=True)
        srv_thread.start()
        time.sleep(3)    
        otest.authorize()

    def test_authorize(self):
        otest.auth_test()


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
statusbar = QtWidgets.QStatusBar()
widget.addWidget(mainwindow)
widget.setFixedSize(501,590)
widget.show()
sys.exit(app.exec_())







