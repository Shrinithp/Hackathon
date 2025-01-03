from flask import Flask, jsonify, request, redirect, Blueprint
from webapi.businessLogic.custom_group_BL import GroupBL
from webapi.businessLogic.mail_BL import MailBL
from webapi.validator.token_validator import TokenValidator

custom_group_bp = Blueprint('NVGroup', __name__)

@custom_group_bp.route('/getGroupEmail', methods=['GET'])
def get_group_email():
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token is missing or invalid"}), 401
    user_info = TokenValidator.validate_access_token(access_token)

    if not user_info:
        return jsonify({"error": "Access token is missing or invalid"}), 401

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401

    group_id = request.args.get('group_id')
    
    return GroupBL.get_group_email(user_id, group_id)

@custom_group_bp.route('/syncMail', methods=['POST'])
def sync_mail(): 
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token is missing or invalid"}), 401
    user_info = TokenValidator.validate_access_token(access_token)

    if not user_info:
        return jsonify({"error": "Access token is missing or invalid"}), 401

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401
    
    response = MailBL.get_mail(access_token)
    GroupBL.sync_mail(user_id, response)
    return jsonify({"success": True})

@custom_group_bp.route('/getMailResponse', methods=['POST'])
def get_mail_response():
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token is missing or invalid"}), 401
    user_info = TokenValidator.validate_access_token(access_token)

    if not user_info:
        return jsonify({"error": "Access token is missing or invalid"}), 401

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401
    
    data = request.get_json()
    mail_body = data.get('mail_body')
    return jsonify({"response":  GroupBL.get_mail_response(mail_body)}),200

@custom_group_bp.route('/getMailSummary', methods=['POST'])
def get_mail_summary():
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token is missing or invalid"}), 401
    user_info = TokenValidator.validate_access_token(access_token)

    if not user_info:
        return jsonify({"error": "Access token is missing or invalid"}), 401

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401
    
    data = request.get_json()
    mail_body = data.get('mail_body')
    return jsonify({"summary":  GroupBL.get_email_summary(mail_body)}),200
