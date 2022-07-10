

import os
import win32com.client as win32

class emailer:

	def create_email(to, subject, attachment_path):
		olApp = win32.Dispatch('Outlook.Application')
		olNS = olApp.GetNameSpace('MAPI')
		mail_item = olApp.CreateItem(0)
		mail_item.Subject = subject
		mail_item.BodyFormat = 1
		mail_item.Body = 'hello world'
		mail_item.To = to
		mail_item.Display(False)
		mail_item.Attachments.Add(attachment_path)

