from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
import pickle
import webbrowser
import os
from urllib.parse import urlparse
from urllib.parse import parse_qs


# params_dict = {}

# if os.path.exists('params.pickle'):

#     with open('params.pickle', 'rb') as i:
        
#         url_ = pickle.load(i)
        
#         parsed_url = urlparse(url_)


#         print(parsed_url)
#         print(parse_qs(parsed_url.query))

#         # url_state = parse_qs(parsed_url.query)["state"][0]
#         # url_realmId = parse_qs(parsed_url.query)["realmId"][0]
#         # url_code = parse_qs(parsed_url.query)["code"][0]

#         # params_dict.update(code=url_code, realmId=url_realmId, state=url_state)

#         # print(params_dict)

# else:
#     pass

#Globals to register the callback values

auth_state = 'eE6p9ZbMquT1F8E2WDAeWmDS8qPbso'
auth_code_1 = 'AB11663306015rvD83yjZ4PO3PKfcuxZc7skNSjFOzT838pVv2'
realm_id = '4620816365213833550'

app_id = "AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7"
app_key = "9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL"


auth_client = AuthClient(
    app_id,
    app_key,
    "http://localhost:8000/",
    "sandbox"
)


def auth_test():
    try:
        tqw = auth_client.get_bearer_token(auth_code_1, realm_id=realm_id)
        print(tqw)
    except AuthClientError as e:
        # just printing here but it can be used for retry workflows, logging, etc
        print(e.status_code)
        print(e.content)
        print(e.intuit_tid)

    
def authorize():
    print("authorize!")
    auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    webbrowser.open(auth_url)
    # response = request.session().get(auth_url)
    # print(response)


    # try:
    #     intuit_oauth.get_bearer_token(AUTH_CODE, realm_id=REALM_ID)
    #     TOKEN = intuit_oauth.state_token
    #     print(f"state_token is {TOKEN}, refresh_token is {intuit_oauth.refresh_token}")
    # except AuthClientError as e:
    #     print(f"chingada madre {e}")

