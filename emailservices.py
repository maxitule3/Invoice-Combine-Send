import database
import win32com.client as win32
from customer import Customer, CustomerFactory
from invoice import Invoice


class CustomerEmail:
    def __init__(self, 
                 customer_name:str='', 
                 customer_email:str='', 
                 cc_email:str='', 
                 attachment_path:str='', 
                 email_body:str=''):
        
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.cc_email = cc_email
        self.attachment_path = attachment_path
        self.email_body = email_body




def format_html_template(invoice_object:Invoice, custom_body=''):
    with open('template.html', 'r', encoding='utf-8') as file:
        html_template = file.read()

    # Assuming invoice_object has attributes that match the placeholders in the template
    formatted_html = html_template.format(
        DocNum=invoice_object.DocNum,
        terms=invoice_object.terms,
        due_date=invoice_object.due_date,
        balance=invoice_object.balance,
        current_company=invoice_object.current_company,
        customer_refrence=invoice_object.customer_refrence,
        customer_name=invoice_object.customer_name,
        invoice_Id=invoice_object.invoice_Id,
        custom_body=custom_body
    )

    return formatted_html


def get_email_body(invoice_object:Invoice, custom_body='', use_custom_body=0):

    # Unpacking the invoice object's attributes into the function
    if use_custom_body == 2:
        formatted_email_body = format_html_template(invoice_object, custom_body)

    elif use_custom_body == 0:
        formatted_email_body = format_html_template(invoice_object, custom_body)

    return formatted_email_body


def construct_email(invoice_object:Invoice, customer_object:Customer, cc_email:str, attachment_path:str, email_body:str):

    email_subject = f'{invoice_object.current_company} - Invoice {invoice_object.DocNum} // {customer_object.name} - {invoice_object.customer_refrence}'

    olApp = win32.Dispatch('Outlook.Application')
    olNS = olApp.GetNameSpace('MAPI')
    mail_item = olApp.CreateItem(0)
    mail_item.Subject = email_subject
    mail_item.BodyFormat = 1
    mail_item.HTMLBody = (email_body)
    mail_item.To = customer_object.email.replace(',',';')
    mail_item.CC = cc_email.replace(',',';')
    mail_item.Display(False)
    mail_item.Attachments.Add(attachment_path)

