from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv
from webapi.service.socketio import socketio
from webapi.controller.mail_controller import auth_bp
from webapi.controller.websocket_controller import socket_bp
from webapi.controller.preference_controller import preference_bp
from webapi.repository.db import db

load_dotenv()

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return 'Hello world'

app.config['SECRET_KEY'] = 'your_secret_key'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/NVMail')
app.register_blueprint(socket_bp, url_prefix='/NVSocket')
app.register_blueprint(preference_bp, url_prefix='/NVPreference')

# PostgreSQL connection URI (without sslmode)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DBConnectionString")
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Initialize socket.io
socketio.init_app(app)

# Enable CORS
CORS(app)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
