from flask import Flask, jsonify, request, redirect, Blueprint
from webapi.businessLogic.preference_BL import GroupBL
from webapi.validator.token_validator import TokenValidator

preference_bp = Blueprint('NVPreference', __name__)
group_BL = GroupBL()
validator = TokenValidator()

@preference_bp.route('/addGroup', methods=['POST'])
def add_group():
    access_token = request.authorization.token
    if not access_token or not access_token.startswith("Bearer "):
        return jsonify({"error": "Access token is missing or invalid"}), 401

    access_token = access_token.replace("Bearer ", "").strip()
    user_info = validator.validate_access_token(access_token)

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401

    data = request.get_json()
    group_name = data.get('group_name')
    if not group_name:
        return jsonify({"error": "Group name is required"}), 400

    result = group_BL.addGroup(group_name, user_id)
    return jsonify(result)

@preference_bp.route('/get_groups', methods=['GET'])
def get_groups():
    access_token = request.authorization.token
    if not access_token or not access_token.startswith("Bearer "):
        return jsonify({"error": "Access token is missing or invalid"}), 401

    access_token = access_token.replace("Bearer ", "").strip()
    user_info = validator.validate_access_token(access_token)

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401

    result = group_BL.get_groups(user_id)
    return jsonify(result)

@preference_bp.route('/delete_group/<int:group_id>', methods=['DELETE'])
def delete_user_from_group(group_id):
    access_token = request.authorization.token
    if not access_token or not access_token.startswith("Bearer "):
        return jsonify({"error": "Access token is missing or invalid"}), 401

    access_token = access_token.replace("Bearer ", "").strip()
    user_info = validator.validate_access_token(access_token)

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401

    result = group_BL.delete_user_from_group(user_id, group_id)
    return jsonify(result)
