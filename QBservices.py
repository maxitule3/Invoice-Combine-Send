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
	access_token='eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..kuzRPv5hEbdYbxx2ObO75Q.92YeOg_I4fgkxjp-dXRK1IqPN7yXQY1hMNp6_fAAsMbs68KyNBfnATci92vuIkq6gGzueAz4lNb3CSQk2O6Ys-PzhAEleVsH2n_wljUXHpgwIdMGeXif-_WG_SE8Ly4xHSXuRedeebWUq-cw1yGrD4U9to_gHc-3mT_Ud8FVVVCdMee2grJ3oj43E-uD_iWKaYbmnyt7MJiSEMsZY8gvzOE7ftrxXr65rCsvAk6eT11RyMCuH4f18Wb-_RuPLA1tVEn5A8hZZf-PVC4UdwfkiLOF8NhHKdc5vlc3PdBuNLzpzw4kCOaKaokIdeJUWceztdUUcNEqmwaL3tETypHrnx9FwealksjuOe5Z-iS8Tlu_mdr2tXWsWpWsXnezjK_5itF0bTebyQkYRGzUIudThHB020iO6ltmdWF1qaLrqiRYxvkOd9EZzWt3qvfiCjZq3LhBid3CgS-UaYGj3e2-BtFjYnKznQrfppvkfJYmzq_Q6Nwzh3H9vXUDFJY0igSYT8Xs7PHPjIvEq15s7fw0X0FnzM5GXvl54_hA2IuKafZCH-XyJaoBCXZfnp9sdIn3o_xBvRLVdZeZEywMrOaTSr_p0zg8LdyP0pgueR-g-WQc3A3x5-DgMsAGF64WTeckDYELge55tVX69LKOaf-lvE-EIpYKCeu-f377rYr7RauDfoRf7ltTFGh5lrkc7RNk0D-hIVTRQ1a7HsWc9x3T1MM9HqCAIm0KG0D59wvENdNRtpdLQCFZKEQljelmdfE0nhEiyoD-S4i_A49fUjMJf3s2vSB2eBS8tbMCmE--gDHIDAjmSyG-Rfs59rp5Db-Xbp5FkcMrJdsSIpkpvlnWLXqJqSBzI5kYSYGxyKM7Qo5ezLGc2gEEqqVM6Mf6W-Kk.Q_Jyk7IbG_aX3pHYx0a-Gg',
	environment='sandbox',
	redirect_uri='http://localhost:8000/callback',
	)

client = QuickBooks(
	auth_client=auth_client,
	refresh_token='AB11661290758nF0VfCeP9BShU1hzChmnmXkpXx39mgreoVySI',
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
	#Downloads a Pdf of invoice. This takes invoice id and file path as arguments

		invoice = Invoice()
		invoice.Id = inv_id
		responce = invoice.download_pdf(qb=client)
		# return responce
		inv_pdf_path = temp_path+'\\'+str(inv_id)+'temp'+'.pdf'
		with open(inv_pdf_path, 'wb')as file:
			file.write(responce)
		return inv_pdf_path

	def get_customer_email():
		print('hi')
