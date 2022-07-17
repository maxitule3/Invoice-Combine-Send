import os
import sys
from intuitlib.enums import Scopes
from intuitlib.client import AuthClient
import json
from quickbooks import QuickBooks
from quickbooks.objects import Account, Attachable, Invoice, Customer


auth_client = AuthClient(
	client_id='AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7',
	client_secret='9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL',
	access_token='eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..8uMAMoH3BVieubLPiUH3Wg.7wfXE1vhu8avFysxzrf3XxdkTNZJ1i5f8FyudrzoQVcjKn5yhccQ54vN2-Wj2-6VUilV2oJtehGVIGOn2QRZWpcCoRjRgVrOmhO74n3Domp8V6N4ZoVQ17tcodPXduGTDLe4HE4BuSHqtyuozLdcTTZJjTJ9ktVVsPy1M63gcTWaooQd1cTXTZqawOifkUiPJjogZDYD2eNvR1vAVbEt4Jj2YKb1Pbg18fo0cGnszrhmYN2SCZC4_GEZXBNCgKLv1ya-pTUssH6li1f12QTBr5NOsdh8DXUd9Lmgzz0ixvK1GBuMk3ujeHxiB8A1QQasK3Lx-1lH5LGppVA0uQhyMZyUvJmShVFLFrf-yBUBcEPT0qGLit_FIu4CO3ShTC0LMqq3FTyA4s-30xhy_GAUtpYSuMefOdHykY6aWHJneXAt9MprCW5rxl73CEXi-iRbxjJfVCOgjE0JZ_diCydXbD5IPpArbTfAgTKS0nWR6E6gUQUY7PUCLVcJ__Mbu45uEo19tB90gD4qTJU5uO7K4woUl4xRuL6xgAYV3fhEUhKmp00PHsWz994oTQ06d_jqT4KLhgpNBasxFbT95aTNRiMXWarnnyuNhxqYzDyVhcodKYTh6j9Q83rAsX5UEwXuCcu1KXwSClKFl-xFOR0rNSTOR60-03QWm0rF9qJyo9zaFAnla6Fz35BfLZtgHxOh8j0OPK7ega5yLAGbd5DHrb9WYZHcAO2DvwHSPGnGJth8yC71cbBOgNyyHJ4RKQgADszOdUY00GdaLvDNTXv0am-dP-jyy0sP-DVAyY7NNK52jECXFaljACBw52_n5HhDUQjciliHtAqA09KT7v1kef22gmaKmFH35nvOjCH_0NTflTqAJYs0ZrsCi3fykX3v.1SVbjRuXv7dM7IeDqZIOKA',
	environment='sandbox',
	redirect_uri='http://localhost:8000/callback',
	)

client = QuickBooks(
	auth_client=auth_client,
	refresh_token='AB11666759872XUiCfknE1GLYK5HaopDqDZgy3a919bMXNwAaG',
	company_id='4620816365213833550',
	minorversion=63
	)


class qb_operations(Invoice, Customer):


	def get_id(inv_num):

		#returns id number using DocNumber aka invoice number ***this is not the inv id***
		#when using filter method, you are always returned a list

		responce = Invoice.filter(DocNumber=f'{inv_num}', qb=client)
		for inv in responce:
			json_data = inv.to_json()
			inv_dict = json.loads(json_data)
			return str(inv_dict["Id"])

	@staticmethod
	def dwnld_pdf(inv_id,temp_path):
	#Downloads a Pdf of invoice. This takes invoice id and file a temporary file path as arguments

		invoice = Invoice()
		invoice.Id = inv_id
		responce = invoice.download_pdf(qb=client)
		# return responce
		inv_pdf_path = temp_path+'\\'+str(inv_id)+'temp'+'.pdf'
		with open(inv_pdf_path, 'wb')as file:
			file.write(responce)
		return inv_pdf_path


	def get_all_customers():
	#This will return a list of dictionarys with all customer data

		json_cust = []
		responce = Customer.all(qb=client)
		for customer in responce:
			try:
				json_data = customer.to_json()
				cdict = json.loads(json_data)
				json_cust.append(cdict)
			except:
				pass
		return json_cust

	def get_customer_email(inv_num):
		responce = Invoice.filter(DocNumber=f'{inv_num}', qb=client)
		for inv in responce:
			json_data = inv.to_json()
			inv_dict = json.loads(json_data)
			inv_id = str(inv_dict["Id"])
			inv_cust = str(inv_dict["CustomerRef"]["name"])
		try:	
			resp = Customer.filter(DisplayName=inv_cust, qb=client)
			for cust in resp:
				cust_json_data = cust.to_json()
				cust_dict = json.loads(cust_json_data)

				try:
					cust_email = str(cust_dict["PrimaryEmailAddr"]["Address"])
				except:
					cust_email = None

			return cust_email

		except:
			'''I need to create an error handeler class. I'm just having a comment printed to console for now'''
			print('Inv # provided may not exist')	



	def get_customer_name(inv_num):
		responce = Invoice.filter(DocNumber=f'{inv_num}', qb=client)
		for inv in responce:
			json_data = inv.to_json()
			inv_dict = json.loads(json_data)
			inv_cust = str(inv_dict["CustomerRef"]["name"])

		return str(inv_cust)

	def get_invoice_details(inv_num):
		#This will return a Tuple - (Customer Name, Invoice Balance, Invoice Due date, Pay Term)

		responce = Invoice.filter(DocNumber=f'{inv_num}', qb=client)
		for inv in responce:
			json_data = inv.to_json()
			inv_dict = json.loads(json_data)
			inv_cust = (inv_dict["CustomerRef"]["name"])
			inv_amount = (inv_dict["Balance"])
			inv_due = (inv_dict["DueDate"])
			inv_term = (inv_dict["SalesTermRef"]["name"])

		return inv_cust, inv_amount, inv_due, inv_term
