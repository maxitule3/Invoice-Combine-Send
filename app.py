import os
import sys
import time
import AppServices
import webbrowser
import threading
import QBservices
import sqlite3

from AppServices import Customer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyPDF2 import PdfFileMerger
from QBservices import qb_operations

from datetime import datetime



class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		loadUi('Main.ui',self)
	
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
		self.pushButton_7.clicked.connect(self.start_authorization)
		self.pushButton_9.clicked.connect(self.get_access_token)
		self.pushButton_11.clicked.connect(self.save_settings)
		self.pushButton_10.clicked.connect(self.revoke_all_tokens)

	def revoke_all_tokens(self):
		self.console_log(str(QBservices.revoke_token()))

	def load_settings(self):

		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()
		c.execute("SELECT * FROM userpref")
		responce = c.fetchone()

		self.lineEdit_5.setText(responce[0])
		self.spinBox.setValue(responce[1])
		self.lineEdit_3.setText(responce[4])
		self.lineEdit_4.setText(responce[5])
		self.lineEdit.setText(responce[2])
		self.lineEdit_2.setText(responce[3])


	def save_settings(self):
		cc_value = self.lineEdit_5.text()
		inv_char_amount = self.spinBox.value()
		sender_in = self.lineEdit_3.text()
		sender_out = self.lineEdit_4.text()
		combiner_in = self.lineEdit.text()
		combiner_out = self.lineEdit_2.text()

		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()
		c.execute("UPDATE userpref SET cc_email=:value", {'value': cc_value})
		conn.commit()
		c.execute("UPDATE userpref SET inv_spinbox=:value", {'value': inv_char_amount})
		conn.commit()
		c.execute("UPDATE userpref SET combine_in=:value", {'value': combiner_in})
		conn.commit()
		c.execute("UPDATE userpref SET combine_out=:value", {'value': combiner_out})
		conn.commit()
		c.execute("UPDATE userpref SET send_in=:value", {'value': sender_in})
		conn.commit()
		c.execute("UPDATE userpref SET send_out=:value", {'value': sender_out})
		conn.commit()
		conn.close()
		self.console_log('Settings saved!')


	def error_window(self, title, message):
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText(message)
			msgBox.setWindowTitle(title)
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
			
	def console_log(self, message):
		current_time = datetime.now()
		dt_string = current_time.strftime('%H:%M:%S')
		self.textEdit_3.append(f'[{dt_string}] : {message}\n \n')
		self.textEdit_2.append(f'[{dt_string}] : {message}\n \n')

	def start_authorization(self):
		# srv_thread = threading.Thread(target=server.start_srv, daemon=True)
		# srv_thread.start()
		# time.sleep(3)
		QBservices.authorize()

	def get_access_token(self):
		QBservices.auth_test()

	def updateCombinerCount(self):
		numberOfItems = self.listWidget.count()
		self.label_16.setText(str(numberOfItems))

	def refreshCombinerList(self):
		self.listWidget.clear()

		if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
			self.error_window('Error', 'Input and Output can\'t be empty')
			self.console_log('Couldn\'t refresh Combiner list')
		else:
			i = self.lineEdit.text()
			folderPath = i.replace('/','\\\\')
			fileNames = os.listdir(i)
			pdf_files = []
			for fileName in fileNames:
				if fileName.endswith('.pdf'):
					pdf_files.append(fileName)
			
			for pdf_file in pdf_files:
				item = QListWidgetItem(pdf_file)
				self.listWidget.addItem(item)
			self.console_log('Combiner list Refreshed')			
			numberOfItems = self.listWidget.count()
			self.label_16.setText(str(numberOfItems))

	def refresh_sender_list(self):
		if self.lineEdit_3.text() == '' or self.lineEdit_4.text() == '':
			self.error_window('Error', 'Input and Output can\'t be empty')
			self.console_log('Couldn\'t refresh Sender list')
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
			self.console_log('Sender list refreshed!')

	def combineAll(self):
		allItems = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
		for item in allItems:
			print(item[0:5])

	def send_selected(self):
		if self.listWidget_2.currentItem() == None:
			self.console_log('Nothing selected from Send list')

		else:
			selected_num = self.spinBox.value()
			output_path = self.lineEdit_4.text()
			item = self.listWidget_2.currentItem()
			item_name = item.text()
			i = (self.lineEdit_3.text() + '\\' + item_name)
			inv_path = i.replace('/','\\')
			output = (output_path + '\\' + item_name)

			try:
				QBservices.check_token()
				inv = item_name[0:selected_num]
				inv_tuple = qb_operations.get_invoice_details(inv)
				inv_terms = inv_tuple[3]
				inv_balance = inv_tuple[1]
				inv_date = inv_tuple[2]
				customer_name = inv_tuple[0]
				customer_ref = inv_tuple[4]
				cc_string = self.lineEdit_5.text()
			
				for i in Customer.customers:
					if i.name == customer_name:
						if i.prt == True:

							webbrowser.open(inv_path)
							sent_item = self.listWidget_2.currentRow()
							self.listWidget_2.takeItem(sent_item)
							self.console_log(f'{inv} was printed!')

						elif i.prt == False:
							if self.checkBox.checkState() == 2:

								email_custom = self.textEdit.toHtml()
								AppServices.emailer.create_email(i.email, f' Wise Transport, LLC - Invoice {inv} // {customer_name} - {customer_ref}', inv_path, email_custom, cc_string)
								sent_item = self.listWidget_2.currentRow()
								self.listWidget_2.takeItem(sent_item)
								self.console_log(f'{inv} was sent!')
								
								if self.checkBox_2.checkState() == 2:
									webbrowser.open(inv_path)
								else:
									pass

							else:
								AppServices.emailer.create_invoice_email(i.email, f' Wise Transport, LLC - Invoice {inv} // {customer_name} - {customer_ref}', inv_path, inv, inv_date, inv_terms, inv_balance, cc_string)
								sent_item = self.listWidget_2.currentRow()
								self.listWidget_2.takeItem(sent_item)
								self.console_log(f'{inv} was sent!')

								if self.checkBox_2.checkState() == 2:
									webbrowser.open(inv_path)
								else:
									pass
								
				items_count = self.listWidget_2.count()
				self.label_17.setText(str(items_count))

			except:
				self.console_log('Error with Quickbooks API call - Invoice number may not exist in QuickBooks')

	def combineSelected(self):
		if self.listWidget.currentItem() == None:
			self.console_log('Nothing selected from Combine list')

		else:

			output_path = self.lineEdit_2.text()
			item = self.listWidget.currentItem()
			itemText = item.text()
			in_path = (self.lineEdit.text() + '\\' +itemText)
			pod_path = in_path.replace('/', '\\')
			selected_num = self.spinBox.value()
			try:
				QBservices.check_token()
				invId = qb_operations.get_id(itemText[0:selected_num])
				inv_pdf = qb_operations.dwnld_pdf(invId,output_path)

				merger = PdfFileMerger()
				merger.append(pod_path)
				merger.merge(0, inv_pdf)
				merger.write(output_path + '\\' + itemText[:-4] + ' -C' + '.pdf')
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
				self.console_log('Error Combining! - Invoice number may not exist in Quickbooks')	

	def refresh_customer_list(self):
		
		QBservices.check_token()
		self.listWidget_3.clear()
		Customer.customers.clear()
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

			Customer.new(cName, cEmail, False)

	def refresh_prt_state(self):
		all_items = [self.listWidget_3.item(x) for x in range(self.listWidget_3.count())]

		for i in all_items:
			state = False
			
			if i.checkState() == 2:
				state = True
			Customer.update_prt(i.text(), state)

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
widget.setWindowTitle('PDF Combine-Send')
widget.show()
mainwindow.load_settings()
sys.exit(app.exec_())