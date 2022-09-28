from AppServices import db_operations as db
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
import webbrowser
import os




app_id = "AB1Q6F1f7BWpIdLcEaTIW3UIXdyigjCeaSLQ5seIEt6eIxD5i7"
app_key = "9p0V0MuWAYE8VKLg7ba6MLSVDJZwdzr7RBA5P6LL"


intuit_oauth = AuthClient(
    app_id,
    app_key,
    "http://localhost:8000/",
    "sandbox"
)

def auth_test():

    state = db.get_oauth('state')
    auth_code = db.get_oauth('code')
    realm_id = db.get_oauth('realm')

    try:
        intuit_oauth.get_bearer_token(auth_code, realm_id=realm_id)

        db.update_value('qbauth', 'token', intuit_oauth.access_token)
        db.update_value('qbauth', 'refresh_token', intuit_oauth.refresh_token)

        db.update_token_expire()


    except AuthClientError as e:
        # just printing here but it can be used for retry workflows, logging, etc
        print(e.status_code)
        print(e.content)
        print(e.intuit_tid)

def get_new_token():
    intuit_oauth.refresh(refresh_token=db.get_oauth('refresh_token'))


def authorize():
    auth_url = intuit_oauth.get_authorization_url([Scopes.ACCOUNTING])
    webbrowser.open(auth_url)
