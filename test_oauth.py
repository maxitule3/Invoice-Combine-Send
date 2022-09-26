import fastapi
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import requests
import uvicorn
import os
import test
import threading
import webbrowser
import Constants

# set up fastAPI
from intuitlib.exceptions import AuthClientError
from requests import Response

app = fastapi.FastAPI()

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

@app.get("/authorize")
def authorize(request: fastapi.Request):
    #print("authorize!")
    auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    #print(f"auth url is {auth_url}")
    #os.system(f"open \"{auth_url}\"")
    # On shitty-ass Windows
    webbrowser.open(auth_url)
    #response = request.session().get(auth_url)


def authorize_1():
    print("authorize!")
    auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    webbrowser.open(auth_url)

@app.get("/oauth")
def get_oauth(request: fastapi.Request):
    print("oauth!")
    print("oauth request incoming")
    STATE = request.query_params.get("state")
    AUTH_CODE = request.query_params.get("code")
    REALM_ID = request.query_params.get("realmId")



    # try:
    #     auth_client.get_bearer_token(AUTH_CODE, realm_id=REALM_ID)
    #     TOKEN = auth_client.state_token
    #     return f"state_token is {TOKEN}, refresh_token is {auth_client.refresh_token}"
    # except AuthClientError as e:
    #     print(e.status_code)
    #     print(e.content)
    #     print(e.intuit_tid)

def start_srv():
    # """
    # This starts up a local webserver on port 8000, and you kick off the oauth flow by hitting
    # http://localhost:8000/authorize
    # ¡ORALE!

    # To use this in your app, you'd add a button that opened that URL in a window, then store the returned
    # code in an object that the app had access to.
    # """
    uvicorn.run("test_oauth:app", host="0.0.0.0", port=8000, reload=True)


# class Oauth_func():
#     def get_token():
#         return(refresh_tok)



# if __name__ == '__main__':
#     main()
