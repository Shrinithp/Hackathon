from webapi.repository.graph_service import GraphService
from flask import Flask, jsonify, request, redirect
import requests
from webapi.repository.model import Email_model


class MailBL:
    def getloginUrl():
        graph_service = GraphService(access_token=None)
        return graph_service.getloginUrl()

    def get_mail(access_token):
        graph_service = GraphService(access_token)
        return graph_service.get_mail()
    
    def send_mail(access_token,email_model):
        try:
            # Convert EmailModel to a dictionary
            email_data = email_model.to_dict()

            # Pass email data to GraphService
            graph_service = GraphService(access_token)
            response = graph_service.send_mail(email_data)
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}