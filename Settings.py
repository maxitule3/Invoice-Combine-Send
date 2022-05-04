from intuitlib.client import AuthClient

auth_client = AuthClient(
        client_id='CLIENT_ID',
        client_secret='CLIENT_SECRET',
        access_token='ACCESS_TOKEN',  # If you do not pass this in, the Quickbooks client will call refresh and get a new access token. 
        environment='sandbox',
        redirect_uri='http://localhost:8000/callback',
    )


client = QuickBooks(
        auth_client=auth_client,
        refresh_token='REFRESH_TOKEN',
        company_id='COMPANY_ID',
    )