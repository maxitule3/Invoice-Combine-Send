import os
import sys
from intuitlib.enums import Scopes
from intuitlib.client import AuthClient
from intuitlib.exceptions import AuthClientError
import webbrowser
import json
from quickbooks import QuickBooks
from quickbooks.objects import Account, Attachable, Invoice, Customer
from AppServices import db_operations as db
from datetime import datetime, timedelta
import sqlite3


intuit_oauth = AuthClient(
	client_id='ABDv92UgFiyYHsfcoWme4xmF267A57czAhZNdHWV0kqQfJK2XY',
	client_secret=db.get_oauth('app_key'),
	access_token=db.get_oauth('token'),
	environment='production',
	redirect_uri='https://example.com/',
	)

def client():

	return	QuickBooks(
		auth_client=intuit_oauth,
		refresh_token=db.get_oauth('refresh_token'),
		company_id=db.get_oauth('realm'),
		minorversion=63
		)


def auth_test():
    state = db.get_oauth('state')
    auth_code = db.get_oauth('code')
    realm_id = db.get_oauth('realm')

    try:
        intuit_oauth.get_bearer_token(auth_code, realm_id=realm_id)

        db.update_value('qbauth', 'token', intuit_oauth.access_token)
        db.update_value('qbauth', 'refresh_token', intuit_oauth.refresh_token)

        db.update_token_expire()


    except AuthClientError as e:
        # just printing here but it can be used for retry workflows, logging, etc
        print(e.status_code)
        print(e.content)
        print(e.intuit_tid)


def get_new_token():
    intuit_oauth.refresh(refresh_token=db.get_oauth('refresh_token'))


def authorize():
    auth_url = intuit_oauth.get_authorization_url([Scopes.ACCOUNTING])
    return(auth_url)
    

def check_token():
	conn = sqlite3.connect('appdata.db')
	c = conn.cursor()

	c.execute("SELECT next_token FROM qbauth")
	responce = c.fetchone()
	date_time_obj = datetime.strptime(responce[0], "%Y-%m-%d %H:%M:%S")
	

	#if True, Then a new token is required
	if date_time_obj < datetime.now():
		try:
			intuit_oauth.refresh(refresh_token=db.get_oauth('refresh_token'))
			db.update_token_expire()
			db.update_value('qbauth', 'token', intuit_oauth.access_token)

		except:
			print('Failed getting new access token')
	else:
		pass

def revoke_token():
	intuit_oauth.revoke()

	conn = sqlite3.connect('appdata.db')
	c = conn.cursor()

	c.execute("UPDATE qbauth SET next_generate=NULL")
	conn.commit()
	c.execute("UPDATE qbauth SET code=NULL")
	conn.commit()
	c.execute("UPDATE qbauth SET state=NULL")
	conn.commit()
	c.execute("UPDATE qbauth SET realm=NULL")
	conn.commit()
	c.execute("UPDATE qbauth SET next_token=NULL")
	conn.commit()
	c.execute("UPDATE qbauth SET token=NULL")
	conn.commit()
	c.execute("UPDATE qbauth SET refresh_token=NULL")
	conn.commit()
	conn.close()

class qb_operations(Invoice, Customer):


	def get_id(inv_num):

		#returns id number using DocNumber aka invoice number ***this is not the inv id***
		#when using filter method, you are always returned a list

		responce = Invoice.filter(DocNumber=f'{inv_num}', qb=client())
		for inv in responce:
			json_data = inv.to_json()
			inv_dict = json.loads(json_data)
			return str(inv_dict["Id"])


	def dwnld_pdf(inv_id,temp_path):

	#Downloads a Pdf of invoice. This takes invoice id and a temporary file path as arguments

		invoice = Invoice()
		invoice.Id = inv_id
		responce = invoice.download_pdf(qb=client())
		# return responce
		inv_pdf_path = temp_path+'\\'+str(inv_id)+'temp'+'.pdf'
		with open(inv_pdf_path, 'wb')as file:
			file.write(responce)
		return inv_pdf_path


	def get_all_customers():

	#This will return a list of dictionarys with all customer data

		json_cust = []
		responce = Customer.all(max_results=1000, qb=client())
		for customer in responce:
			try:
				json_data = customer.to_json()
				cdict = json.loads(json_data)
				json_cust.append(cdict)
			except:
				pass
		return json_cust


	def get_customer_email(inv_num):

		#This will return the customers email as a string

		responce = Invoice.filter(DocNumber=f'{inv_num}', qb=client())
		for inv in responce:
			json_data = inv.to_json()
			inv_dict = json.loads(json_data)
			inv_id = str(inv_dict["Id"])
			inv_cust = str(inv_dict["CustomerRef"]["name"])
		try:	
			resp = Customer.filter(DisplayName=inv_cust, qb=client())
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

		responce = Invoice.filter(DocNumber=f'{inv_num}', qb=client())
		for inv in responce:
			json_data = inv.to_json()
			inv_dict = json.loads(json_data)
#			inv_cust = str(inv_dict["CustomerRef"]["name"])
			inv_cust = str(inv_dict)
		return str(inv_cust)


	def get_invoice_details(inv_num):

		#This will return a Tuple - (Customer Name, Invoice Balance, Invoice Due date, Pay Term)

		responce = Invoice.filter(DocNumber=f'{inv_num}', qb=client())
		for inv in responce:
			json_data = inv.to_json()
			inv_dict = json.loads(json_data)
			inv_cust = (inv_dict["CustomerRef"]["name"])
			inv_amount = (inv_dict["Balance"])
			inv_due = (inv_dict["DueDate"])
			inv_term = (inv_dict["SalesTermRef"]["name"])
			customer_ref = (inv_dict["CustomField"][0]["StringValue"])

		return inv_cust, inv_amount, inv_due, inv_term, customer_ref