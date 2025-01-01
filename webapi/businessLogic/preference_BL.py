from flask import Flask, jsonify, request, redirect
from webapi.repository.preference_repository import GroupService


class GroupBL:
    def addGroup(group_name, user_id):
        preference_service = GroupService()
        return preference_service.add_group(group_name, user_id)
    
    def get_groups(user_id):
        preference_service = GroupService()
        return preference_service.get_groups(user_id)
    
    def delete_user_from_group(user_id, group_id):
        preference_service = GroupService()
        return preference_service.delete_user_from_group(user_id, group_id)