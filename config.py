import json


#enter 'Production' for a production environment and 'Sandbox' for a sandbox environment
ENVIRONMENT = 'Production' 
REDIRECT_URI = 'https://example.com/'




with open('config.json') as f:
    json_data = json.load(f)


def get_api_key():
    if ENVIRONMENT == 'Production':
        return json_data['api_key']
    else:
        return json_data['sandbox_api_key']


def get_api_secret():
    if ENVIRONMENT == 'Production':
        return json_data['api_secret']
    else:
        return json_data['sandbox_api_secret']


def get_environment():
    if ENVIRONMENT == 'Production':
        production_url = 'https://quickbooks.api.intuit.com'
        return production_url
    
    else:
        sandbox_url = 'https://sandbox-quickbooks.api.intuit.com'
        return sandbox_url
