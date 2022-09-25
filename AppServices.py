import os
import win32com.client as win32

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
<p><span style="font-size:12.0pt;font-family:&quot;Arial&quot;,sans-serif">------------------------   Invoice Summary  --------------------------<span style="color:black"><br>
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
