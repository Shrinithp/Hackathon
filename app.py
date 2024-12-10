from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from webapi.controller.mailController import auth_bp


load_dotenv()

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/NVMail')
#PostgreSQL connection URI (without sslmode)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DBConnectionString")


app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


