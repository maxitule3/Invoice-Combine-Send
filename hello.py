
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

class MainWindow(QDialog):
	def __init__(self):
		super(MainWindow,self).__init__()
		loadUi('dummygui.ui',self)
		self.button.clicked.connect(self.browse)

	def browse(self):
		fname = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
		self.line.setText(fname)






app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
sys.exit(app.exec_())
