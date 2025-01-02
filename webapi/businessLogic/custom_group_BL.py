from flask import Flask, jsonify, request, redirect
from webapi.repository.custom_group_repository import GroupService

class GroupBL:
    def get_group_email(user_id, group_id):
        group_service = GroupService()
        return group_service.get_group_email(user_id, group_id)
    
    def sync_mail(user_id, response):
        group_service = GroupService()
        return group_service.sync_mail(user_id, response)