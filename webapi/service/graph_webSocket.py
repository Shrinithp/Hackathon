import requests
from datetime import datetime, timedelta

def create_subscription(access_token):
    url = "https://graph.microsoft.com/v1.0/subscriptions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Ensure expirationDateTime is in the correct ISO 8601 format with 'Z' for UTC
    expiration_time = (datetime.utcnow() + timedelta(minutes=4230)).isoformat() + "Z"

    data = {
        "changeType": "created,updated",  # Correct change type
        "notificationUrl": "https://hackathon-nvmail.onrender.com/NVSocket/webhook",  # Your webhook URL
        "resource": "me/messages",  # Correct resource
        "expirationDateTime": expiration_time,  # Ensure expiration time is properly formatted
        "clientState": "secretClientValue"  # Custom client state for validation
    }
    
    # Send the POST request to create the subscription
    response = requests.post(url, headers=headers, json=data)
    
    # Return the response in JSON format
    return response.json()

