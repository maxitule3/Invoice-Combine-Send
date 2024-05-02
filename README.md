# Invoice-Combine-Send

This app integrates with QuickBooks Online, allowing you to merge QuickBooks invoices with PDFs on your device. The Purpose of this app is to make invoicing customers that require their invoice along with back-up paperwork faster and more efficient.

Once connected, you will be able to pull a list of all your customers from quickbooks and choose which ones require printed invoices and which ones require an email.


# Instructions

1. Clone repository
2. Create a file named config.json and structure as shown below...
3. {
    "sandbox_api_key": "insert_key_here",
    "sandbox_api_secret":"insert_key_here",
    "api_key":"insert_key_here",
    "api_secret":"insert_key_here"
}

4. Configure config.py by changing "ENVIRONMENT" to either "Production" or "Sandbox"
5. Launch app.py


# Version Notes

Beta 2 - Added multiple company support, Fixed Combine all bug where app would crash upon completion, Customers print status is now saved