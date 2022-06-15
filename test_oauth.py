import fastapi
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import requests
import uvicorn
import os

# set up fastAPI
from intuitlib.exceptions import AuthClientError
from requests import Response

app = fastapi.FastAPI()

# Globals to register the callback values
STATE = ""
AUTH_CODE = ""
REALM_ID = ""

app_id = "ABoFQA2csmWne0isXdLLsLhQS2UB5Co0FBJ1HoMZWb2pDem2rI"
app_key = "Bzfyqe4wb4brTtepkmstCqMCWm6Gbm2pxQsyt3hH"


intuit_oauth = AuthClient(
    app_id,
    app_key,
    "http://localhost:8000/oauth",
    "sandbox"
)

@app.get("/authorize")
def authorize(request: fastapi.Request):
    print("authorize!")
    auth_url = intuit_oauth.get_authorization_url([Scopes.ACCOUNTING])
    print(f"auth url is {auth_url}")
    os.system(f"open \"{auth_url}\"")
    # On shitty-ass Windows
    # os.system("start \"\" https://example.com")
    # response = requests.session().get(auth_url)

@app.get("/oauth")
def get_oauth(request: fastapi.Request):
    print("oauth!")
    print("oauth request incoming")
    STATE = request.query_params.get("state")
    AUTH_CODE = request.query_params.get("code")
    REALM_ID = request.query_params.get("realmId")

    try:
        intuit_oauth.get_bearer_token(AUTH_CODE, realm_id=REALM_ID)
        TOKEN = intuit_oauth.state_token
        return f"state_token is {TOKEN}, refresh_token is {intuit_oauth.refresh_token}"
    except AuthClientError as e:
        print(f"chingada madre {e}")


def main():
    """
    This starts up a local webserver on port 8000, and you kick off the oauth flow by hitting
    http://localhost:8000/authorize
    ¡ORALE!

    To use this in your app, you'd add a button that opened that URL in a window, then store the returned
    code in an object that the app had access to.
    """
    uvicorn.run("test_oauth:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()