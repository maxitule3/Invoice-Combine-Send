from company import CompanyToken
from typing import List
from customer import Customer, CustomerFactory
from invoice import Invoice
import oauthservices
import requests
import config


def get_company_info(company_token:CompanyToken):
    base_url = config.get_environment()
    url = f'{base_url}/v3/company/{company_token.realm_id}/companyinfo/{company_token.realm_id}'
    headers = {
        'Authorization': f'Bearer {company_token.access_token}',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_dict = response.json()

    elif response.status_code == 401:
        oauthservices.refresh_authclient(company_token=company_token)
        get_company_info(company_token)


def get_all_customers(company_token:CompanyToken)->List[Customer]:
    oauth_client = oauthservices.get_base_client(company_token)
    base_url = config.get_environment()
    select_statement = "SELECT * FROM Customer maxresults 800"
    url = f'{base_url}/v3/company/{oauth_client.realm_id}/query?query={select_statement}'
    headers = {
        'Authorization': f'Bearer {oauth_client.access_token}',
        'Accept': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        oauth_client.refresh()
        oauthservices.update_access_token(oauth_client)
        headers = {
        'Authorization': f'Bearer {oauth_client.access_token}',
        'Accept': 'application/json'}
        response = requests.get(url, headers=headers)

    response_dict = response.json()
    customers_data_list = response_dict['QueryResponse']['Customer']

    for customer_data in customers_data_list:
        try:
            customer_name = customer_data["DisplayName"]
        except:
            customer_name=''
        try:
            customer_email = customer_data["PrimaryEmailAddr"]["Address"]
        except:
            customer_email=''
        customer_object = CustomerFactory.create_customer(customer_name=customer_name, customer_email=customer_email)
        CustomerFactory.upsert_customer(customer_object)
        customer_object_list = CustomerFactory.get_all()

    return customer_object_list


def get_invoice_pdf(company_token:CompanyToken, invoice_id):
    oauth_client = oauthservices.get_base_client(company_token)
    base_url = config.get_environment()
    url = f'{base_url}/v3/company/{company_token.realm_id}/invoice/{invoice_id}/pdf'
    headers = {
        'Authorization': f'Bearer {oauth_client.access_token}',
        'Accept': 'application/pdf'}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        oauth_client.refresh()
        oauthservices.update_access_token(oauth_client)
        headers = {
        'Authorization': f'Bearer {oauth_client.access_token}',
        'Accept': 'application/pdf'}
        response = requests.get(url, headers=headers)

    return response.content


def get_invoice_by_DocNumber(company_token:CompanyToken, invoice_DocNumber, tag_value=0)->Invoice:
    oauth_client = oauthservices.get_base_client(company_token)
    base_url = config.get_environment()
    select_statement = f"SELECT * FROM Invoice WHERE DocNumber = '{invoice_DocNumber}'"
    uri = f'{base_url}/v3/company/{company_token.realm_id}/query?query={select_statement}&minorversion=70'
    headers = {
        'Authorization': f'Bearer {oauth_client.access_token}',
        'Accept': 'application/json'}
    
    response = requests.get(uri, headers=headers)

    if response.status_code == 401:
        oauth_client.refresh()
        oauthservices.update_access_token(oauth_client)
        headers = {
        'Authorization': f'Bearer {oauth_client.access_token}',
        'Accept': 'application/json'}
        response = requests.get(url=uri, headers=headers)

    #parse the API responce
    response_dict = response.json()
    invoice_data_list = response_dict['QueryResponse']['Invoice']

    #Map vallues of responce to invoice object, then return that object
    invoice_Id = invoice_data_list[0]['Id']
    customer_name = invoice_data_list[0]["CustomerRef"]["name"]
    invoice_balance = invoice_data_list[0]["Balance"]
    due_date = invoice_data_list[0]["DueDate"]
    invoice_terms = invoice_data_list[0]["SalesTermRef"]["name"]
    try:
        customer_refrence = invoice_data_list[0]["CustomField"][tag_value]["StringValue"]
    except:
        customer_refrence = ''

    invoice_object = Invoice(invoice_Id=invoice_Id,
                             DocNum=invoice_DocNumber,
                             current_company=company_token.company_name,
                             balance=invoice_balance,
                             due_date=due_date,
                             terms=invoice_terms,
                             customer_name=customer_name,
                             customer_refrence=customer_refrence)

    return invoice_object
