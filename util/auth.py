from github import Auth, Github, GithubIntegration
from dotenv import load_dotenv
import os
import base64

load_dotenv()

key = os.getenv("KEY").encode("ascii")
key_bytes = base64.b64decode(key)
private_key = key_bytes.decode("utf-8")

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")

access = Auth.AppAuth(app_id=GITHUB_APP_ID, private_key=private_key)
gi = GithubIntegration(auth=access)
installation_id = ''
for installation in gi.get_installations():
    installation_id = installation.id

auth = Auth.AppAuth(app_id=GITHUB_APP_ID, private_key=private_key).get_installation_auth(installation_id)
g = Github(auth=auth)


def get_token():
    return auth.token

