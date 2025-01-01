# webapi/controller/websocket_controller.py

from flask import Blueprint, jsonify, request
from webapi.service.socketio import socketio  # Import from the service
from webapi.service import graph_webSocket
from flask_socketio import emit
from webapi.validator.token_validator import TokenValidator

# Create a Blueprint for WebSocket routes
socket_bp = Blueprint('NVSocket', __name__)

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Connected to Flask WebSocket server'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

# Webhook route to handle notifications from Graph API
@socket_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # Check if the validation token exists
        validation_token = request.args.get('validationToken')
        if validation_token:
            print(f"Received validation token: '{validation_token}'")
            # Respond with the validation token as required by Microsoft Graph
            return validation_token, 200

        # Handle notifications
        data = request.get_json()
        if data:
            print("New notification from Graph API:", data)

            # Process notifications if present
            if 'value' in data:
                for notification in data['value']:
                    resource = notification.get('resource', 'Unknown resource')
                    resource_id = notification.get('resourceData', {}).get('id', 'Unknown ID')
                    print(f"Received notification: '{resource}', ID: {resource_id}")

            # Emit the notification data to the frontend via Socket.IO
            socketio.emit('new_mails', {'mails': data})

        return '', 200
    except Exception as e:
        print(f"Error handling webhook: {str(e)}")
        return '', 500
    
    
# Create a subscription for the user after login
@socket_bp.route('/createSubscription', methods=['POST'])
def create_subscription():
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token not provided"}), 400
    user_info = TokenValidator.validate_access_token(access_token)

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401
    response = graph_webSocket.create_subscription(access_token,user_id)
    return response
