import requests
from flask import jsonify

class TokenValidator:
    def validate_access_token(access_token):
        url = "https://graph.microsoft.com/v1.0/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Token is valid
            return response.json()
        else:
            # Token is invalid
            return None
