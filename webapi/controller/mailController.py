from flask import Flask, jsonify, request, redirect, Blueprint
import requests
from webapi.application.mailService import MailService

auth_bp = Blueprint('NVMail', __name__)
@auth_bp.route('/login',methods=['GET'])
def login():
    auth_url = MailService.getloginUrl()
    return jsonify({"auth_url": auth_url})

@auth_bp.route('/getMail', methods=['GET'])
def get_mail():
    try:
        access_token = request.authorization.token
        if not access_token:
            return jsonify({"error": "Access token not provided"}), 400

        response = MailService.get_mail(access_token)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

