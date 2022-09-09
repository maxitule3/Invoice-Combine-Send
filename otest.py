from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from requests import Response, request

import webbrowser
import sys
import os
import shutil

# Globals to register the callback values
STATE = ""
AUTH_CODE = ""
REALM_ID = ""

app_id = "AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7"
app_key = "9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL"


auth_client = AuthClient(
    app_id,
    app_key,
    "http://localhost:8000/oauth",
    "sandbox"
)


def authorize():
    print("authorize!")
    auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    response = request.session().get(auth_url)
    print(response)



def get_oauth():
    print("oauth!")
    print("oauth request incoming")
    STATE = request.query_params.get("state")
    AUTH_CODE = request.query_params.get("code")
    REALM_ID = request.query_params.get("realmId")

    try:
        intuit_oauth.get_bearer_token(AUTH_CODE, realm_id=REALM_ID)
        TOKEN = intuit_oauth.state_token
        print(f"state_token is {TOKEN}, refresh_token is {intuit_oauth.refresh_token}")
    except AuthClientError as e:
        print(f"chingada madre {e}")

