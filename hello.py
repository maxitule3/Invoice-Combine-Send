
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QMimeData

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		loadUi('QBICST.ui',self)

		self.CombineInputButton.clicked.connect(self.setInputFolderCombine)
		self.CombineOutputButton.clicked.connect(self.setOutputFolderCombine)
		self.toolButton_4.clicked.connect(self.setInputFolderSender)
		self.toolButton_3.clicked.connect(self.setOutputFolderSender)
		self.pushButton.clicked.connect(self.refreshCombinerList)
		self.pushButton_3.clicked.connect(self.combineAll)
		self.pushButton_4.clicked.connect(self.combineSelected)


	def updateCombinerCount(self):
		numberOfItems = self.listWidget.count()
		self.label_16.setText(str(numberOfItems))


	def refreshCombinerList(self):
		self.listWidget.clear()
		i = self.lineEdit.text()
		folderPath = i.replace('/','\\\\')
		fileNames = os.listdir(folderPath)
		
		for fileName in fileNames:
			item = QListWidgetItem(fileName)
			self.listWidget.addItem(item)
		
		numberOfItems = self.listWidget.count()
		self.label_16.setText(str(numberOfItems))


	def combineAll(self):
		allItems = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
		for item in allItems:
			print(item[0:5])

	def combineSelected(self):
		item = self.listWidget.currentItem()
		itemText = item.text()
		print(itemText[0:5])

		i = self.listWidget.currentRow()
		self.listWidget.takeItem(i)

		numberOfItems = self.listWidget.count()
		self.label_16.setText(str(numberOfItems))


	def setInputFolderCombine(self):
		fname = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
		self.lineEdit.setText(fname)

	def setOutputFolderCombine(self):
		fname = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
		self.lineEdit_2.setText(fname)

	def setInputFolderSender(self):
		fname = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
		self.lineEdit_3.setText(fname)

	def setOutputFolderSender(self):
		fname = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
		self.lineEdit_4.setText(fname)
		senderOutputPath = self.lineEdit_4.text()



app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
statusbar = QtWidgets.QStatusBar()
widget.addWidget(mainwindow)
widget.setFixedSize(501,590)
widget.show()
sys.exit(app.exec_())
