from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
import webbrowser
import os

from AppServices import db_operations as db


app_id = "AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7"
app_key = "9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL"


intuit_oauth = AuthClient(
    app_id,
    app_key,
    "http://localhost:8000/",
    "sandbox"
)

def auth_test():

    state = db.get_state()
    auth_code = db.get_code()
    realm_id = db.get_realmId()

    try:
        intuit_oauth.get_bearer_token(auth_code, realm_id=realm_id)
        db.update_token(intuit_oauth.access_token)
        db.update_refresh(intuit_oauth.refresh_token)

        


    except AuthClientError as e:
        # just printing here but it can be used for retry workflows, logging, etc
        print(e.status_code)
        print(e.content)
        print(e.intuit_tid)

    
def authorize():
    auth_url = intuit_oauth.get_authorization_url([Scopes.ACCOUNTING])
    webbrowser.open(auth_url)
