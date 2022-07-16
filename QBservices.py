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
	access_token='eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..f0Qc-lhhIoWj1QQNDX3dKg.SO6TYLSL3Yt6p48F7WC8YtaKdXOeVaGG2JE6_0Rm3oKMwGOdHYX1DuEwWheSIhjCLd3c-7qU2sKYbeNPAG8j8EQ4G_jH1hE4mhBSCS5XMd4FrS0XmRovyFgSdtspnbg_8H_SqdpxQjIpW0LC8uyZjBh2VRWMDIooeqHt1FnV7QLN-lkT_Thz-Rp8K9u7-atCnbS56RBIo-Gn03O15SMlvTagZvwWix4uQXOp1_bkUnSlYGVUfEC94vKykyjYItN1qtADwWwOQCeGvMVMO3v5o9w59fNXuZL9jzYGsnBZzRfum20UV2eM14tzF1W8j8aqbAQxmwhikINNsjVObBxXtDoSaYDSzjW2tubuUD9kfv00kKdrhhPvKRlYPRM86xDPdJ8pMB5kt5GNZaiYafCht0wwkEIbAi6_VPHS6rjiS6VJIJRAFr1elytDu69_4YyGhFdJrViJ0zSGIl-A6aztyvmyMC8v2-oA-PLHaoZ5S7ISTySZa_Y4jAgKIlW3glAO6i3qnofI0YwvIrI89ieYYg4ZHUqIL3fCJ9fSH5SoMgEOc_gNkKG7H9uhC5tuDypXpHE6IR5XVHVyQfGqvzqKbPeQPsPoX4eNSmwc1eAHrTO1rK_NM_FBU9b8iNMaOAzdtuRRILF2NOzcJqVCrxtIkSfjkhxO0T_A8ANRFQrWMm86Z62XkXfXHeQt-BS22ruBTC2y-NdBo4QFhiDDEMqz5K7wbddA6iXOdxDug6wbIKnA9yG3ARNokHAzpKdM2E54uMJwc8enZBn5b6ozBpwtX2vr-QSQZ_S1ik-_QlNNELxe-C1hAo-LE-ZL_zAbez6LWW8th-9O3EVA_guGBoFbKekscCCB4P1o_EiDTBTDuFWWhKTU6Qvv957JH4RHxuS2.oS6ij9_UuCBk5ez9AJK1Zg',
	environment='sandbox',
	redirect_uri='http://localhost:8000/callback',
	)

client = QuickBooks(
	auth_client=auth_client,
	refresh_token='AB11666664350PEvHnrBmz64rwHlgWrZbRANUlWBxJM5mzJ5zC',
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

