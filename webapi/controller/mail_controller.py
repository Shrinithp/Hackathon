from flask import Flask, jsonify, request, redirect, Blueprint
import requests
from webapi.businessLogic.mail_BL import MailBL
from webapi.repository.model import Email_model

auth_bp = Blueprint('NVMail', __name__)
@auth_bp.route('/login',methods=['GET'])
def login():
    auth_url = MailBL.getloginUrl()
    return jsonify({"auth_url": auth_url})

@auth_bp.route('/getMail', methods=['GET'])
def get_mail():
    try:
        access_token = request.authorization.token
        if not access_token:
            return jsonify({"error": "Access token not provided"}), 400

        response = MailBL.get_mail(access_token)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/sendMail', methods=['POST'])
def send_mail():
    try:
        # Parse JSON request body into EmailModel
        data = request.json
        access_token = request.authorization.token
        email_model = Email_model.EmailModel.from_dict(data)

        # Pass the email model to the MailService
        response = MailBL.send_mail(access_token,email_model)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

