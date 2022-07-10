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
	access_token='eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..J5tm2lSbPHrw_eHh1HM4Mw.enXqi0nZT5lrx5bhRlN8uVoXId12zTFuDSO3hRsvXG0u1xW1sKGzSgZSe6rPnAdTwRlwA2IyWs7LNd-wSUntycMxd2P3EBEUy_xz7I33eiq42L3GJLWQ35-8xoqTCricSDqBFgPKT7Pr6kpQ_EGj2meO_MBO-pUSyvIXzATVpwBM3uKI_XaRCTllSoNlWLpC2PLmuoZ6WtHBda7mGN1lZlkPbV9yZIT-UXhJTqNpZWurB_plyLO60c5IijO3uhyOGlDsTG_8HdLhXdmeOopsxM5bVSiR1jW1sATbfBqx7fU8QnG7oHVeZNcqk6yLbWv1hJkMcSXFdtMnhMql9hI8ci4HJ1pZy45Z10349IxHPCbsa5WzmQkLPb2Bean9gXz8S3I1jI0S_7Co16dbivkM06p2CMK8vwN6iQicM86RJEJu54kX6_vOhTk1iZ9MQySZFHQRAKpdAQ75CHmmVKbmGrmGoKIlb97lL4Uut0BnWg0CwrhzZn4Gp9Yb-xrGKs1BtbwoqikHA-PDJk30s-_oCF7lCo0IcO9BMEPVlmKI5vwXKbNBk0leRvHPpwF9nrtAITtFQtPq8Yln-XVjKqy2zYOgc1P03w_qetZ47_HqSu_skDpAIhESMNt6xee0aYlgOZhrrCi9TZDRkL6jlbpNaG42GnUDgNz69YMPSht4Q2D7ym-SlO8JUbQ9VQpPZel3ivyeHP2xEsEmQpNPRREz9lwd0DXweYVjCJvb2fJJ68A2PszKRjoPO4_Kz0Re9bBNVm_SKk2P2Li00-Wexe6lfbx3R3t1EfrigORikRiiFhaH0VVZONplhKn6iHSmpmiAmyA-rC1g9BifUzOEQ6EeAhqJ6rifcf6HQxcAxo-rpcfEwVuhUFATi4POqayPZC-z.fXoA6ryu8SJndXYcOCfnsw',
	environment='sandbox',
	redirect_uri='http://localhost:8000/callback',
	)

client = QuickBooks(
	auth_client=auth_client,
	refresh_token='AB11666148815nmvyPV4qmgTg5012OXrWcxvGw7a11bbHWBzuo',
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

		return inv_cust