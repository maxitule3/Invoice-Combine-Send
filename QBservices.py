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
	access_token='eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..LHjIkHyjT3qwO7eWJpJVOQ.koMUHrumNbxVYwwc4IRqKmbuTcjIeXgRJfPT0W0xti35rDfmfb6trGCluxCASaamoW8BKlHNwM4csMQLB0Ig5kBcuLPXS3oTVZzF4LgS8uzrVefatENAtflF_5WNnqr2pOD4RkyskfgjI3dQ3ZdZ7HP3rez_AQk5opjXneh-aX63HjB10JAOWw_-Xu9JovIh4QSx45xFTezAo82oSuEK7xUUDFhT3ZkcEeBiSb_WiWKs2YgDzWB9_WjU1lQ_CbK8qGibnTQ2CMR6T-zytL8BeBNXqVOtjv2Bz_d6z7jPtrUnbvEJHWbHSmm5_3keq-Ho14XHELjP8a9bKocwU8fgNcX1LIctLB9wOwQhAMzX0ueG_R3ea55F9c4vmoB8LuPx_3_rlWnDDqXoOorLkawsBah3BeV3yfDPyhDlNHYSpX9VlnKa7LqTGTeDeo7Z0KjiPztTmgcrDFZsR4BxamioCwni-P34Hrjxcv52QoYIlopjtxWHKBIFbb44ggOAYyNPnGDINfaEMa0E4R3F5iq5Raatc5dZORAmPduMw6O1ghlT_NGhqlAwbb2XzrkIH9rA6sUb8HG-dt-s9qnmvGq2pH-zFkkpt-ec6yUEBEnTMvtt83dtgYawBe0MIOGF5x0bxh_gQelaV1KUSfBqXvTw68bmW-2OjXMpfzj0aZKNAMn9hi_vqErUZMwJcunoEaoC5eR3VleM8vS7qTh-WxSGg14yehbOqRMC1xs4JKgjL9xWznF_DAe7z9AMA0jyPjpCIvxeU_uv-23CrCXUJESQATSY4z0dhb9kuvBlurhIoXRXNtAUsDqLjv4qQUUfHuLLHR_OymONQhyJjozAwo7RbhmQDzsOJhnuNe3NHCu7FJwLn7SBb2kmsJkm5GYNGZS5.Vr5prxLKqmOc96lI7HS67g',
	environment='sandbox',
	redirect_uri='http://localhost:8000/callback',
	)

client = QuickBooks(
	auth_client=auth_client,
	refresh_token='AB11661487994mJPAPjy1ZXpO4RVZ3l4mfLXO8nwUg53rvI4xb',
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
		return(json_cust)

