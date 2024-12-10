import msal
from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv
import requests

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPES = os.getenv("SCOPES")
baseUrl=os.getenv("baseUrl")
authority_url = os.getenv("authority_url")
REDIRECT_URI = os.getenv("REDIRECT_URI")

msal_app = ConfidentialClientApplication(
    client_id = CLIENT_ID,
    client_credential=CLIENT_SECRET
)

class GraphService:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api_url = "https://graph.microsoft.com/v1.0/me/"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        self.msal_app = ConfidentialClientApplication(
        client_id = os.getenv("CLIENT_ID"),
        client_credential = os.getenv("CLIENT_SECRET")
        )
        self.scopes = ['User.Read', 'Mail.Read', 'Mail.Send']

    def getloginUrl(self):
        
        return msal_app.get_authorization_request_url(scopes=self.scopes) 

    def get_mail(self):
        response = requests.get(self.api_url + 'mailFolders/Inbox/messages/delta', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching emails: {response.text}")