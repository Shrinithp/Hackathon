from flask import Flask, jsonify, request, redirect, Blueprint
from webapi.businessLogic.preference_BL import GroupBL
from webapi.validator.token_validator import TokenValidator

preference_bp = Blueprint('NVPreference', __name__)

@preference_bp.route('/addGroup', methods=['POST'])
def add_group():
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
    group_name = data.get('group_name')
    group_description = data.get('description')
    if not group_name:
        return jsonify({"error": "Group name is required"}), 400

    result = GroupBL.addGroup(group_name,group_description, user_id)
    return jsonify(result)

@preference_bp.route('/get_groups', methods=['GET'])
def get_groups():
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token is missing or invalid"}), 401

    user_info = TokenValidator.validate_access_token(access_token)

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401

    result = GroupBL.get_groups(user_id)
    return jsonify(result)

@preference_bp.route('/delete_group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token is missing or invalid"}), 401

    user_info = TokenValidator.validate_access_token(access_token)

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401

    result = GroupBL.delete_group(user_id, group_id)
    return jsonify(result)

@preference_bp.route('/edit_group', methods=['PUT'])
def edit_group():
    access_token = request.authorization.token
    if not access_token:
        return jsonify({"error": "Access token is missing or invalid"}), 401

    user_info = TokenValidator.validate_access_token(access_token)

    user_id = user_info.get("id")

    if not user_info:
        return jsonify({"error": "Invalid or expired access token"}), 401
    
    data = request.get_json()
    group_id = data.get('id')
    group_name = data.get('group_name')
    group_description = data.get('description')

    result = GroupBL.edit_group(user_id, group_id, group_name, group_description)
    return jsonify(result)
