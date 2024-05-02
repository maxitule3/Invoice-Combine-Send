from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QListWidgetItem, QToolBar, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs
from company import CompanyTokenFactory
from customer import CustomerFactory
from appsettings import UserSettings, UserSettingsFactory
import emailservices
import pdfservices
import quickbooksservices
import webbrowser
import oauthservices
import os
import sys
import database


class WebWindow(QMainWindow):
    #Initializes internet browser window and buttons
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Authenticate')
        self.setFixedSize(900, 700)
        
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        self.doneButton = QPushButton()
        self.doneButton.setText('Done')
        self.doneButton.clicked.connect(self.get_url_tokens)

        toolbar.addWidget(self.doneButton)
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        self.web_view.load(QUrl(oauthservices.get_oauth_url()))


    def get_url_tokens(self):
        url_string = self.web_view.url().toString()
        parsed_url = urlparse(url_string)

        try:
            captured_code = parse_qs(parsed_url.query)['code'][0]
            captured_realmid = parse_qs(parsed_url.query)['realmId'][0]
 
        except:
            print('Error getting parameters from url or commiting values to DataBase')
            return

        company_token = oauthservices.get_tokens(realm_id=captured_realmid,access_code=captured_code)
        CompanyTokenFactory.upsert(company_token=company_token)
        mainwindow.load_ui()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi('Main.ui',self)

        self.CombineInputButton.clicked.connect(self.set_combiner_input_folder)
        self.CombineOutputButton.clicked.connect(self.set_combiner_ouput_folder)
        self.toolButton_4.clicked.connect(self.set_sender_input_folder)
        self.pushButton_7.clicked.connect(self.start_authorization)
        self.customer_refresh_button.clicked.connect(self.refresh_customer_list)
        self.listWidget_3.itemChanged.connect(self.update_customers_print_status)
        self.pushButton.clicked.connect(self.combiner_refresh_list)
        self.pushButton_2.clicked.connect(self.sender_refresh_list)
        self.pushButton_4.clicked.connect(self.combine_one)
        self.pushButton_3.clicked.connect(self.combine_all)
        self.pushButton_5.clicked.connect(self.send_one)
        self.pushButton_11.clicked.connect(self.save_user_settings)


    def console_log(self, message):
        current_time = datetime.now()
        dt_string = current_time.strftime('%H:%M:%S')
        self.textEdit_3.append(f'[{dt_string}] : {message}\n \n')
        self.textEdit_2.append(f'[{dt_string}] : {message}\n \n')


    def load_ui(self):
        #this will get companies from db and add them to the comboBox
        all_companies = CompanyTokenFactory.get_all()

        for company_token in all_companies:
            self.comboBox.addItem(company_token.company_name)

        user_settings = UserSettingsFactory.get_user_settings()
        
        self.spinBox_2.setValue(user_settings.tag_number_value)
        self.lineEdit_5.setText(user_settings.cc_email)
        self.spinBox.setValue(user_settings.invoice_length)
        self.lineEdit.setText(user_settings.combiner_input)
        self.lineEdit_2.setText(user_settings.combiner_output)
        self.lineEdit_3.setText(user_settings.sender_input)
        self.checkBox.setCheckState(user_settings.use_custom_body)
        self.textEdit.setText(user_settings.custom_body)


    def save_user_settings(self)->None:
        #Fetches all values from user interface and stores them in DB
        user_settings = UserSettings(tag_number_value=self.spinBox_2.value(),
                                     cc_email=self.lineEdit_5.text(),
                                     invoice_length=self.spinBox.value(),
                                     combiner_input=self.lineEdit.text(),
                                     combiner_output=self.lineEdit_2.text(),
                                     sender_input=self.lineEdit_3.text(),
                                     use_custom_body=self.checkBox.checkState(),
                                     custom_body=self.textEdit.toPlainText())
        user_settings.save_settings()


    def start_authorization(self):
        self.web = WebWindow()
        self.web.show()


    def get_company_token(self):
        currently_selected_company = self.comboBox.currentText()
        token = CompanyTokenFactory.get_one(str(currently_selected_company))

        return token
    

    def refresh_customer_list(self):
        #Get list of all customer
        currently_selected_company = self.comboBox.currentText()
        token = CompanyTokenFactory.get_one(str(currently_selected_company))
        try:
            all_customers_list = quickbooksservices.get_all_customers(token)
        except:
            self.console_log('Error getting customer list, Do you have a company selected?')
            return

        self.listWidget_3.clear()

        for customer in all_customers_list:
            item = QListWidgetItem(customer.name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable) # type: ignore

            if customer.wants_invoice_printed == 2:
                item.setCheckState(QtCore.Qt.Checked) # type: ignore

            else:
                item.setCheckState(QtCore.Qt.Unchecked) # type: ignore

            self.listWidget_3.addItem(item)


    def update_customers_print_status(self):
        QList_items = [self.listWidget_3.item(x) for x in range(self.listWidget_3.count())]
        customers_object_list = []

        for QList_item in QList_items:
            customer_name = QList_item.text()#<- this is the customer in QtItem form
            QChecked_status = QList_item.checkState() #<- Int 0 or 2
            customer_object = CustomerFactory.create_customer(customer_name=customer_name, wants_invoice_printed=QChecked_status)
            customers_object_list.append(customer_object)

        CustomerFactory.bulk_upsert_print_status(customers_object_list)


    def save_setting(self):
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute("")


    def set_combiner_input_folder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
        self.lineEdit.setText(folder_path)


    def set_combiner_ouput_folder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
        self.lineEdit_2.setText(folder_path)


    def set_sender_input_folder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
        self.lineEdit_3.setText(folder_path)


    def set_sender_output_folder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
        self.lineEdit_4.setText(folder_path)
        senderOutputPath = self.lineEdit_4.text()


    def combiner_refresh_list(self)->None:
        self.listWidget.clear()

        if self.lineEdit.text() == '' or self.lineEdit_2.text() == '':
            #self.error_window('Error', 'Input and Output can\'t be empty')
            self.console_log('Couldn\'t refresh Combiner list - Make sure a folder is selected')

        else:
            line_text = self.lineEdit.text()
            file_name_list = os.listdir(line_text)

            for file_name in file_name_list:

                if file_name.endswith('.pdf'):
                    Qlist_item = QListWidgetItem(file_name)
                    self.listWidget.addItem(Qlist_item)

            self.console_log('Combiner list Refreshed')			
            numberOfItems = self.listWidget.count()
            self.label_16.setText(str(numberOfItems))


    def sender_refresh_list(self):
        self.listWidget_2.clear()

        #Check to see if anything in list is selected
        if self.lineEdit_3.text() == '':
            self.console_log('Couldn\'t refresh Combiner list - Make sure a folder is selected')
            return

        folder_path = self.lineEdit_3.text()
        file_name_list = os.listdir(folder_path)

        for file_name in file_name_list:

            if file_name.endswith('.pdf'):
                Qlist_item = QListWidgetItem(file_name)
                self.listWidget_2.addItem(Qlist_item)

        self.console_log('Combiner list Refreshed')			
        numberOfItems = self.listWidget_2.count()
        self.label_7.setText(str(numberOfItems))


    def combine_one(self):
        currently_selected_company = self.comboBox.currentText()
        token = CompanyTokenFactory.get_one(currently_selected_company)

        if self.listWidget.currentItem() == None:
            self.console_log('Nothing selected from Combine list')

        else:
            character_length = self.spinBox.value()
            selected_item_text = self.listWidget.currentItem().text()
            user_chosen_suffix = self.lineEdit_6.text()
            input_path = self.lineEdit.text() + '/' + selected_item_text
            output_path = self.lineEdit_2.text() + f'/{selected_item_text[:-4]}{user_chosen_suffix}.pdf'

            try:
                #get invoice ID inorder to download pdf then download pdf
                invoice_object = quickbooksservices.get_invoice_by_DocNumber(company_token=token,invoice_DocNumber=selected_item_text[0:character_length])
                inv_pdf = quickbooksservices.get_invoice_pdf(company_token=token, invoice_id=int(invoice_object.invoice_Id))

                #merge pdf with the one downloaded
                pdfservices.merge_pdfs(api_pdf_data=inv_pdf, local_pdf_path=input_path, output_pdf_path=output_path)

                #remove selected item from list
                item = self.listWidget.currentRow()
                self.listWidget.takeItem(item)

                #update number of files label
                numberOfItems = self.listWidget.count()
                self.label_16.setText(str(numberOfItems))

            except:
                    self.console_log('Error Combining! - Invoice number may not exist in Quickbooks')


    def combine_all(self):
        currently_selected_company = self.comboBox.currentText()
        token = CompanyTokenFactory.get_one(currently_selected_company)
        
        #Get is of all items in combiner list as QListWidgetItems
        QList_items = [self.listWidget.item(x) for x in range(self.listWidget.count())]

        if len(QList_items) == 0:
            self.console_log('No items in list to combine!')
            return

        character_length = self.spinBox.value()
        for list_item in QList_items:
            selected_item_text = list_item.text()
            user_chosen_suffix = self.lineEdit_6.text()
            input_path = self.lineEdit.text() + '/' + selected_item_text
            output_path = self.lineEdit_2.text() + f'/{selected_item_text[:-4]}{user_chosen_suffix}.pdf'

            try:
                #get invoice ID inorder to download pdf then download pdf
                invoice_object = quickbooksservices.get_invoice_by_DocNumber(company_token=token,invoice_DocNumber=selected_item_text[0:character_length])
                inv_pdf = quickbooksservices.get_invoice_pdf(company_token=token, invoice_id=int(invoice_object.invoice_Id))

            except:
                self.console_log(f'Error Combining {selected_item_text}! - Invoice number may not exist in Quickbooks')
                return
            
            #merge pdf with the one downloaded
            pdfservices.merge_pdfs(api_pdf_data=inv_pdf, local_pdf_path=input_path, output_pdf_path=output_path)

            #remove selected item from list
            i = self.listWidget.currentRow()
            self.listWidget.takeItem(i)

            #update number of files label
            numberOfItems = self.listWidget.count()
            self.label_16.setText(str(numberOfItems))


    def sender_next_list_item(self):
        current_row_index = self.listWidget_2.currentRow()
        next_row_index = current_row_index + 1 if current_row_index < self.listWidget_2.count() - 1 else 0
        self.listWidget_2.setCurrentRow(next_row_index)


    def send_one(self):
        if self.listWidget_2.currentItem() == None:
            self.console_log('Nothing selected from Sender list')
            return

        #instantiate all nessassary variables
        currently_selected_company = self.comboBox.currentText()
        token = CompanyTokenFactory.get_one(currently_selected_company)
        invoice_character_length = self.spinBox.value()
        selected_item_text = self.listWidget_2.currentItem().text()
        pdf_path = self.lineEdit_3.text() + '/' + selected_item_text
        invoice_DocNumber = selected_item_text[0:invoice_character_length]
        use_custom_email = self.checkBox.checkState()
        custom_body = self.textEdit.toPlainText()
        qb_tag_value = self.spinBox_2.value()-1
        cc_email = self.lineEdit_5.text()

        #get invoice object using Quickbooks API and invoice DocNimber
        try:
            invoice_object = quickbooksservices.get_invoice_by_DocNumber(company_token=token, invoice_DocNumber=invoice_DocNumber, tag_value=qb_tag_value)

        except:
            self.console_log('Error with retriving customer/Possible API call error - invoice may not exist in QB')
            return
        
        #get customer object from DB using customer name
        customer_object = CustomerFactory.get_customer_by_name(customer_name=invoice_object.customer_name)

        #Open PDF using internet browser if customer wants invoice printed
        if customer_object.wants_invoice_printed == 2:
            webbrowser.open_new_tab(pdf_path)
            self.sender_next_list_item()

        #construct and then open email using outlook
        elif customer_object.wants_invoice_printed == 0:

            email_body = emailservices.get_email_body(invoice_object=invoice_object, custom_body=custom_body, use_custom_body=use_custom_email)

            emailservices.construct_email(invoice_object=invoice_object, 
                                          customer_object=customer_object, 
                                          cc_email=cc_email,
                                          attachment_path=pdf_path,
                                          email_body=email_body)
            
            self.sender_next_list_item()

        else:
            self.console_log('Customer Object has invalid print value')


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
statusbar = QtWidgets.QStatusBar()
widget.addWidget(mainwindow)
widget.setFixedSize(501,590)
widget.setWindowTitle('PDF Combine-Send')
widget.show()
mainwindow.load_ui()
#mainwindow.check_connect_status()
sys.exit(app.exec_())