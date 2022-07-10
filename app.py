
import os
import shutil
import sys
import sqlite3
from CustClass import customer
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QMimeData
from PyPDF2 import PdfFileMerger
from QBservices import qb_operations
from datetime import datetime
import AppServices
import webbrowser


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
		self.pushButton_8.clicked.connect(self.refresh_customer_list)
		self.pushButton_2.clicked.connect(self.refresh_sender_list)
		self.pushButton_5.clicked.connect(self.send_selected)
		self.listWidget_3.itemChanged.connect(self.refresh_prt_state)

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

	def refresh_sender_list(self):
		if self.lineEdit_3.text() == '' or self.lineEdit_4.text() == '':
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Input and Output folder can't be empty")
			msgBox.setWindowTitle("Error")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
		else:
			self.listWidget_2.clear()
			i = self.lineEdit_3.text()
			folderPath = i.replace('/','\\\\')
			file_names = os.listdir(i)

			pdf_files = []

			for file_name in file_names:
				if file_name.endswith('.pdf'):
					pdf_files.append(file_name)

			for pdf_file in pdf_files:
				item = QListWidgetItem(pdf_file)
				self.listWidget_2.addItem(item)

			items_count = self.listWidget_2.count()
			self.label_17.setText(str(items_count))



	def combineAll(self):
		allItems = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
		for item in allItems:
			print(item[0:5])


	def send_selected(self):
		if self.listWidget_2.currentItem() == None:

			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Nothing selected from list")
			msgBox.setWindowTitle("Error")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
		else:
			output_path = self.lineEdit_4.text()
			item = self.listWidget_2.currentItem()
			item_name = item.text()
			i = (self.lineEdit_3.text() + '\\' + item_name)
			inv_path = i.replace('/','\\')
			output = (output_path + '\\' + item_name)

			try:
				inv = item_name[0:5]
				customer_name = qb_operations.get_customer_name(inv)

				for i in customer.customers:
					if i['name'] == customer_name:
						if i['prt'] == True:

							webbrowser.open(inv_path)
							time.sleep(5)
							shutil.move(inv_path,output)

						elif i['prt'] == False:

							AppServices.emailer.create_email(i['email'], f'Invoice {inv}', inv_path)
							time.sleep(5)
							shutil.move(inv_path,output)

			except:
				print('Couldnt find customer name with invoice number')


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
			try:

				invId = qb_operations.get_id(itemText[0:5])
				inv_pdf = qb_operations.dwnld_pdf(invId,output_path)

				merger = PdfFileMerger()
				merger.append(pod_path)
				merger.merge(0, inv_pdf)
				merger.write(output_path + '\\' + itemText)
				merger.close()

				os.remove(inv_pdf)
				os.remove(pod_path)


				#removes selected item from list
				i = self.listWidget.currentRow()
				self.listWidget.takeItem(i)

				#updates number of files label
				numberOfItems = self.listWidget.count()
				self.label_16.setText(str(numberOfItems))

			except:
				print('error')	

	def refresh_customer_list(self):

		self.listWidget_3.clear()
		customer.customers.clear()
		current_time = datetime.now()
		dt_string = current_time.strftime("%m/%d/%Y %H:%M:%S")
		self.label_13.setText(dt_string)

		cust_dict = qb_operations.get_all_customers()

		for cust in cust_dict:
			item = QListWidgetItem(cust['DisplayName'])
			item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
			item.setCheckState(QtCore.Qt.Unchecked)
			self.listWidget_3.addItem(item)

			
			try:
				cName = cust['DisplayName']
				cEmail = cust['PrimaryEmailAddr']['Address']

			except:
				cName = cust['DisplayName']
				cEmail = None

			customer.new(cName, cEmail, False)


	def refresh_prt_state(self):
		all_items = [self.listWidget_3.item(x) for x in range(self.listWidget_3.count())]

		for i in all_items:
			state = False
			
			if i.checkState() == 2:
				state = True
			customer.update_prt(i.text(), state)


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