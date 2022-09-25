import os
import sys
from intuitlib.enums import Scopes
from intuitlib.client import AuthClient
import json
from quickbooks import QuickBooks
from quickbooks.objects import Account, Attachable, Invoice, Customer
import sqlite3


auth_client = AuthClient(
	client_id='AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7',
	client_secret='9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL',
	access_token='eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..hcKei0Wwck7UnXmwCtKdkA.DDssrShCwjofy8EH3B3hUQJHJSqZOFylB73FucRvSMbdo6oT-9VlQiAHqA_maEYpXafTtP8a59NAQqqWDnIXNuGltzllr94scpa0cdGXJD5VheCk9HxG5LVfFJqCWj-7DgQf8sDfGWwhINukXuP70ociWLub0hz6Swi9cQfnT2q9vZ2aDd8_I3u3Ie8PFVFdQ4J2NuyuqBiUCd5yomlrcqoeTsb3b2CVG8R6UHSupOKn_ZblO0Q5rViGr9TO40zKvlo2M95x5Buat-Hbl3YylY2DRzkXwOVPX7kqEpcc0U6UvPSuRSI1uY1yEPdjOWHE8x6Wrc04isqoKtdmDallyVpBApu_oHciybvtGe0xFCnVSOtiSKmHdsyZ1fOPlGv_85crXGqACj7rVXEbe9X6zax5fZ73YaROynrqwzdUh4FM1Y03L3dCX88I0PEXBgg7AOC7dAjJYcDbJr7H-QP1AmLwFkVklJ0mtxZgzJnXk0A5O5NycLk7Xb3EBCGiwKT-akLKh7oHBLDPWEd3ovxHRX_zkDDZ3VN6SUl6DV5IBab4sR1OvchTfohafVI4RKL2X21fju0JDwXJgYVcZWl3EFc5IkSRlIpnEkU-yXY5gI1rmjQuQy7nUqoJpsIhhRpZ8ILLC8qkUi09668a_e7gxenmIiBcaayU_q7VYdbZlddxNE3KnoPlaD3SMwhgq0ljRlBtaL60zllrwYCGAm-L_pE_YPWSXjvvtlYWFJNaMA6Srd8JBD5ol6LDpD6qaYQg.cLGBf_Xc5a2d5rOgltUYEg',
	environment='sandbox',
	redirect_uri='http://localhost:8000/callback',
	)

client = QuickBooks(
	auth_client=auth_client,
	refresh_token='AB116683871600wVcf6F8XH1nZ2RyKSV9nmGgO2Aa7l4YDyudS',
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


class db_operations():

	def db_exists():
		result = os.path.exists('appdata.db')
		return(result)

	def customer_exists(customer_name):
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("SELECT * FROM customer_data WHERE customer_name=?", (customer_name,))
		if c.fetchone() == None:
			return False

		else:
			return True

		conn.commit()
		conn.close()