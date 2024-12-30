from flask import Flask, jsonify, request, redirect, Blueprint
preference_bp = Blueprint('NVMail', __name__)

@preference_bp.route('/addGroup',methods=['POST'])
def AddPreference():
    data = request.json
    access_token = request.authorization.token
    return str("Add Preference")

@preference_bp.route('/getGroups',methods=['GET'])
def GetPreference():
    return str("Get Preference")

@preference_bp.route('/deleteGroup',methods=['DELETE'])
def DeletePreference():
    return str("Delete Preference")

    