from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from company import CompanyToken
import database
import requests
import config



def get_oauth_url()->str:
    print('A URL was Requested')
    auth_client = AuthClient( config.get_api_key(), config.get_api_key(), config.REDIRECT_URI, config.ENVIRONMENT )
    url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    return url


def get_tokens(realm_id:str, access_code:str)-> CompanyToken:
    auth_client = AuthClient( config.get_api_key(), config.get_api_secret(), config.REDIRECT_URI, config.ENVIRONMENT )
    auth_client.get_bearer_token(realm_id=realm_id, auth_code=access_code)
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = f'{base_url}/v3/company/{auth_client.realm_id}/companyinfo/{auth_client.realm_id}'
    headers = {
        'Authorization': f'Bearer {auth_client.access_token}',
        'Accept': 'application/json'
    }
    #make API call to recieve quickbooks company name
    try:
        response = requests.get(url, headers=headers)
        response_dict = response.json()
        print('API Call Successful!!! YAY!')
    except:
        #Create better error responce: should return string to app or raise error // not sure yet
        print('Error! Unssuccessful API call, Something went wrong')
    token = CompanyToken(refresh_token=str(auth_client.refresh_token),
                         access_token=str(auth_client.access_token),
                         company_name=str(response_dict['CompanyInfo']['CompanyName']),
                         realm_id=realm_id
                         )
    return token


def get_base_client(company_token:CompanyToken)->AuthClient:
    #company = get_auth_data_by_company_name(company_name)
    return AuthClient(config.get_api_key(), 
                      config.get_api_secret(), 
                      config.REDIRECT_URI, 
                      config.ENVIRONMENT,
                      realm_id=company_token.realm_id, 
                      refresh_token=company_token.refresh_token, 
                      access_token=company_token.access_token)


def refresh_authclient(company_token:CompanyToken)->None:
    auth_client = AuthClient(
        config.get_api_key(),
        config.get_api_secret(),
        config.REDIRECT_URI,
        config.ENVIRONMENT,
        realm_id=str(company_token.realm_id),
        refresh_token=str(company_token.refresh_token),
        access_token=str(company_token.access_token)
        )
    auth_client.refresh()
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE company_token SET access_token = ? WHERE realm_id = ?", (auth_client.access_token,auth_client.realm_id))
    conn.commit()
    conn.close()

def update_access_token(auth_client:AuthClient)->None:
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE company_token SET access_token = ? WHERE realm_id = ?", (auth_client.access_token,auth_client.realm_id))
    conn.commit()
    conn.close