
import os
import shutil
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QMimeData
from PyPDF2 import PdfFileMerger


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

		if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Input and Output folder can't be empty")
			msgBox.setWindowTitle("Error")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
		else:
			i = self.lineEdit.text()
			folderPath = i.replace('/','\\\\')
			fileNames = os.listdir(folderPath)
			pdf_files = []
			for fileName in fileNames:
				if fileName.endswith('.pdf'):
					pdf_files.append(fileName)
			
			for pdf_file in pdf_files:
				item = QListWidgetItem(pdf_file)
				self.listWidget.addItem(item)
			
			numberOfItems = self.listWidget.count()
			self.label_16.setText(str(numberOfItems))


	def combineAll(self):
		allItems = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
		for item in allItems:
			print(item[0:5])

	def combineSelected(self):
		if self.listWidget.currentItem() == None:

			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Nothing selected from list")
			msgBox.setWindowTitle("Failed to combine")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
		else:

			output_path = self.lineEdit_2.text()
			item = self.listWidget.currentItem()
			itemText = item.text()
			in_path = (self.lineEdit.text() + '\\' +itemText)
			pod_path = in_path.replace('/', '\\')
			inv_path = ('C:\\Users\\Maxwell Itule\\Documents\\GitHub\\ProtoEnv\\Assets for Testing\\testinv.pdf')

			merger = PdfFileMerger()
			merger.append(pod_path)
			merger.merge(0, inv_path)
			merger.write(output_path + '\\' + itemText)
			merger.close()

			os.remove(pod_path)


			#removes selected item from list
			i = self.listWidget.currentRow()
			self.listWidget.takeItem(i)

			#updates number of files label
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
