from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from webapi.service.socketio import socketio
from webapi.controller.mail_controller import auth_bp
from webapi.controller.websocket_controller import socket_bp
from webapi.controller.preference_controller import preference_bp


load_dotenv()

app = Flask(__name__)

@app.route('/')
def helloWorld():
    return 'Hello world'

app.config['SECRET_KEY'] = 'your_secret_key'

app.register_blueprint(auth_bp, url_prefix='/NVMail')
app.register_blueprint(socket_bp, url_prefix='/NVSocket')
app.register_blueprint(preference_bp, url_prefix='/NVPreference')

#PostgreSQL connection URI (without sslmode)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DBConnectionString")


app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio.init_app(app)

 
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, keyfile='key.pem', certfile='cert.pem')

    #  app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))


