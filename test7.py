import os
import shutil
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QMimeData
from PyPDF2 import PdfFileMerger
from intuitlib.enums import Scopes
from intuitlib.client import AuthClient
import webbrowser
import json




class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		loadUi('QBICST.ui',self)

		self.pushButton.clicked.connect(self.openurl)


	def openurl(self):
		client_id= 'AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7'
		client_secret = '9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL'
		redirect_uri = 'http://localhost:5000/callback'
		environment = 'Sandbox'
		# 'Production'
		# Set to latest at the time of updating this app, can be be configured to any minor version
		API_MINORVERSION = '23'

		auth_client = AuthClient( client_id, client_secret, redirect_uri, environment )
		url = auth_client.get_authorization_url([Scopes.ACCOUNTING, Scopes.EMAIL, Scopes.OPENID])
		webbrowser.open(url)



app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
statusbar = QtWidgets.QStatusBar()
widget.addWidget(mainwindow)
widget.setFixedSize(501,590)
widget.show()
sys.exit(app.exec_())
