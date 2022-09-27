import os
import win32com.client as win32
import sqlite3

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

	def db_exists():
		result = os.path.exists('appdata.db')
		return(result)

	def update_token(new_token):
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("UPDATE qbauth SET token=:token", {'token': new_token})
		conn.commit()
		conn.close()

	def update_refresh(new_token):
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("UPDATE qbauth SET refresh_token=:token", {'token': new_token})
		conn.commit()
		conn.close()
		
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
	
	def get_code():
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("SELECT code FROM qbauth")
		responce = c.fetchone()[0]
		conn.commit()
		conn.close()
		return(responce)

	def get_state():
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("SELECT state FROM qbauth")
		responce = c.fetchone()[0]
		conn.commit()
		conn.close()
		return(responce)

	def get_realmId():
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("SELECT realm FROM qbauth")
		responce = c.fetchone()[0]
		conn.commit()
		conn.close()
		return(responce)

	def get_token():
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("SELECT token FROM qbauth")
		responce = c.fetchone()[0]
		conn.commit()
		conn.close()
		return(responce)

	def get_refresh():
		conn = sqlite3.connect('appdata.db')
		c = conn.cursor()

		c.execute("SELECT refresh_token FROM qbauth")
		responce = c.fetchone()[0]
		conn.commit()
		conn.close()
		return(responce)

