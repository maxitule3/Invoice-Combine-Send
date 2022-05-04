import os
import shutil
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QMimeData
from PyPDF2 import PdfFileMerger
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import webbrowser
import json



# OAuth2 credentials
client_id= 'AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7'
client_secret = '9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL'
redirect_uri = 'http://localhost:5000/callback'
environment = 'Sandbox'
# 'Production'
# Set to latest at the time of updating this app, can be be configured to any minor version
API_MINORVERSION = '23'

# url='https://www.python.org'
# webbrowser.open(url)

auth_client = AuthClient( client_id, client_secret, redirect_uri, environment )
url = auth_client.get_authorization_url([Scopes.ACCOUNTING, Scopes.EMAIL, Scopes.OPENID])


#webbrowser.open(url)
#auth_client.get_bearer_token(auth_code, realm_id=realm_id)



# base_url = 'https://sandbox-quickbooks.api.intuit.com'
# url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, auth_client.realm_id)
# auth_header = 'Bearer {0}'.format(auth_client.access_token)
# headers = {
# 	'Authorization': auth_header,
# 	'Accept': 'application/json'
# }
# response = requests.get(url, headers=headers)

#print(response)

