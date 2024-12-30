# webapi/controller/websocket_controller.py

from flask import Blueprint, jsonify, request
from webapi.service.socketio import socketio  # Import from the service
from webapi.service import graph_webSocket
from flask_socketio import emit

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
    data = request.json
    if data:
        # Process and emit the Graph API notification
        print("New notification from Graph API:", data)
        socketio.emit('new_mails', {'mails': data})
        return '', 200
    return '', 400

# Create a subscription for the user after login
@socket_bp.route('/createSubscription', methods=['POST'])
def create_subscription():
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token not provided"}), 400
    
    response = graph_webSocket.create_subscription(access_token)
    return response
