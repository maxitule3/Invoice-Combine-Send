# Invoice-Combine-Send

This app integrates with QuickBooks Online, allowing you to merge QuickBooks invoices with PDFs on your device. The Purpose of this app is to make invoicing customers that require their invoice along with back-up paperwork faster and more efficient.

Once connected, you will be able to pull a list of all your customers from quickbooks and choose which ones require printed invoices and which ones require an email.


# Instructions

1. Clone repository
2. Create a file named config.json and structure as shown below...
3. {
    "sandbox_api_key": "AB799PNBZztbbyvxbEiAYdrqaZKJ8AtPTDKd4bGXEynTAX6io0",
    "sandbox_api_secret":"J116EgsHt9m7I7PSjvOPzU62zFH8imHtCrQ0dYi9",
    "api_key":"ABDv92UgFiyYHsfcoWme4xmF267A57czAhZNdHWV0kqQfJK2XY",
    "api_secret":"FJpqo6lyeJZp8WJIUH84osCx2ZD6SMC70sbopWGB"
}

4. Configure config.py by changing "ENVIRONMENT" to either "Production" or "Sandbox"
5. Launch app.py


# Version Notes

Beta 2 - Added multiple company support, Fixed Combine all bug where app would crash upon completion, Customers print status is now saved