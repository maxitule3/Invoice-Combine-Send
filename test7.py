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
from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer
from quickbooks.objects import Invoice
from quickbooks.objects import Account, Attachable


auth_client = AuthClient(
	client_id='AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7',
	client_secret='9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL',
	access_token='eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..xULEp4_CjjnUHoAP19vD3Q.MhIyt-e_MudP0whiLXKpq9RCXKOxy_SNjyETSrnpjQMsH36bIsDvb_viaP198MYmZ_wnbrEYD5uOr-OUteTok12P6AFfIrvKO_ZixIT6X4eIE5TiMZt7WQW06d1zkbijtDXAw8fcnqv9hOir5-hGWj9JyyQg9B9fQvvzWl5SSSUgm0gfTQqr4WgCup1AOugz50UUFWuoi1YJ3i0nxYpClFxzQG9hyn_130_jLouGhqb_H2dg1XbuEw-K7L174IrzlNXIV_7Xc8G4lnm3UswViZlemXSd9fUroK9IIGQRB56PQMX75m2SSVlFkOp0gERphP0kJ1CUD_UzyNIr4pljPYDkGppbccZn0ZdpoYp9d_d4COTmfjcwCziOObquvMIagldRjKxEfaCX6QXhWF6uOHfkrZuBtF2cQVOWmE6vaE5l5WFlXuZ9CoKotJWvtFUk6qIzKGiZy1WuGYWIAtWJhg3qVBA1MVd4ZiLxZA-MT7Nuz8H3cx6StizKLYCLpfsw6msFhkUIM1s5tqQbNIlJ_9rX0ilMEwOh6_9kAVe8oq7NqUubJwI2KKnn7y6G-BoJB3eHugUML1-gkXhag5bV_SkTB9sNFMX2jtX9GGjh4PJMfMLAmFf5GNUpd6_RP2g6kN5lDleGMWs7NtrasTKhpPUubkKK_odpVkDsg3IFwGR3S6qVAxnpR_q0m7khccZOp9tmjZo6-NJ-52o8aF0GUBUsdjCZZhoE7F3X860Y-eru0QZEvGDiSgtCVIFM70R8450GLZwLL7jgwHeg-qjGhQEbC-4sLYvt733G3BxRUU84mY84LBMHU2Na5uyK-SYn1vBDpquxeJ5V8bR44z8O2CTTbfBB0ujt5Q6805q-4MrnJE5m960QspOxXJt4i5RS.eaE_f1OZWJQ3K2RMdNAvNQ',  # If you do not pass this in, the Quickbooks client will call refresh and get a new access token. 
	environment='sandbox',
	redirect_uri='http://localhost:8000/callback',
	)

client = QuickBooks(
	auth_client=auth_client,
	refresh_token='AB1166104994943VUcrMrWheRp4HXhFKk4Spob4l1ed5GcTiLU',
	company_id='4620816365213833550',
	)

client = QuickBooks(
	auth_client=auth_client,
	refresh_token='AB1166104994943VUcrMrWheRp4HXhFKk4Spob4l1ed5GcTiLU',
	company_id='4620816365213833550',
	minorversion=63
	)


inv_list = ['1010','10100','1004']


for inv_num in inv_list:
	#when using filter method, you are always returned a list
	responce = Invoice.filter(DocNumber=inv_num, qb=client)
	for inv in responce:
		data = inv.to_json()
		print(data)

