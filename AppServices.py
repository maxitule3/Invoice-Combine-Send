import os
import win32com.client as win32
import sqlite3
from datetime import datetime, timedelta, date


class emailer():

	def create_email(to, subject, attachment_path, email_body):
	#email body is required to formated in HTML

		olApp = win32.Dispatch('Outlook.Application')
		olNS = olApp.GetNameSpace('MAPI')
		mail_item = olApp.CreateItem(0)
		mail_item.Subject = subject
		mail_item.BodyFormat = 1
		mail_item.HTMLBody = (email_body)
		mail_item.To = to
		mail_item.Display(False)
		mail_item.Attachments.Add(attachment_path)

	def create_invoice_email(to, subject, attachment_path, invoice_numb, invoice_due_date, invoice_term, invoice_amount):
	#creates a table in email body containing invoice details
		html_inv = """\
<html>
<head></head>
<body>
<table border="0" cellspacing="0" cellpadding="0" width="700" style="width:525.0pt;background:#f7f7f7">
<tbody>
<tr>
<td style="padding:15.0pt 15.0pt 15.0pt 15.0pt">
<p><span style="font-size:12.0pt;font-family:&quot;Arial&quot;,sans-serif">--------------------------Invoice--Summary--------------------------<span style="color:black"><br>
Invoice# : <b>{invoice_numb}</b><br>
Invoice Due Date : <b>{invoice_due_date}</b><br>
Terms : <b>{invoice_term}</b><br>
Amount Due : <b>{invoice_amount}</b><br>
<br>
The complete version has been provided as an attachment to this email.<br>
---------------------------------------------------------------------</span><u></u><u></u></span></p>
</td>
</tr>
</tbody>
</table>
</body>
</html>
""".format(**locals())

		olApp = win32.Dispatch('Outlook.Application')
		olNS = olApp.GetNameSpace('MAPI')
		mail_item = olApp.CreateItem(0)
		mail_item.Subject = subject
		mail_item.BodyFormat = 1
		mail_item.HTMLBody = (html_inv)
		mail_item.To = to
		mail_item.Display(False)
		mail_item.Attachments.Add(attachment_path)


class Customer():

	customers = []

	def __init__(self, name, email, prt):
		self.name = name
		self.email = email
		self.prt = prt
	
	def new(name, email, prt):
		cust = Customer(name, email, prt)
		Customer.customers.append(cust)

	def update_prt(name, prt):

		for i in Customer.customers:
			if i.name == name:
				i.prt = prt


class db_operations():

	#Returns Boolan value depending on if db file exist
	def db_exists():
		result = os.path.exists('appdata.db')
		return(result)

	#Updates all rows in specified column/table
	def update_value(table, column, new_value):
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute(f"UPDATE {table} SET {column}=:value", {'value': new_value})
		conn.commit()
		conn.close()

	#Checks if specified customer exists and returns Boolian value
	def customer_exists(customer_name):
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("SELECT * FROM customer_data WHERE customer_name=?", (customer_name,))
		if c.fetchone() == None:
			conn.close()
			return False

		else:
			conn.close()
			return True

	#gets value from first row in the - Takes colum as argument
	def get_oauth(column):
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute(f"SELECT {column} FROM qbauth")
		responce = c.fetchone()[0]
		conn.commit()
		conn.close()
		return(responce)

	#Updates all rows in specified column/table
	def update_value(table, column, new_value):
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute(f"UPDATE {table} SET {column}=:value", {'value': new_value})
		conn.commit()
		conn.close()

	#stores current date + 100 days as a string
	def update_refresh_date():
		date_plus100 = datetime.now() + timedelta(days=100)
		date_string = date_plus100.strftime("%Y-%m-%d")

		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("UPDATE qbauth SET next_generate=:date", {'date': date_string})
		conn.commit()
		conn.close()

	def get_next_generate():
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()
		c.execute("SELECT next_generate FROM qbauth")
		responce = c.fetchone()[0]
		conn.commit()
		conn.close()

		date_time_obj = datetime.strptime(responce, "%Y-%m-%d").date()
		return(date_time_obj)

	def update_token_expire():
		token_time_plus60 = datetime.now() + timedelta(minutes=60)
		datetime_string = token_time_plus60.strftime("%Y-%m-%d %H:%M:%S")

		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("UPDATE qbauth SET next_token=:time", {'time': datetime_string})
		conn.commit()
		conn.close()

	def check_token_expire():
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()
		c.execute("SELECT next_token FROM qbauth")
		responce = c.fetchone()[0]
		conn.commit()
		conn.close()

		date_time_obj = datetime.strptime(responce, "%Y-%m-%d %H:%M:%S")

		if datetime.now() < date_time_obj:
			return False

		else:
			return True