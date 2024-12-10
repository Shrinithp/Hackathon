from webapi.domain.graphService import GraphService
from flask import Flask, jsonify, request, redirect
import requests


class MailService:
    def getloginUrl():
        graph_service = GraphService(access_token=None)
        return graph_service.getloginUrl()

    def get_mail(access_token):
        graph_service = GraphService(access_token)
        return graph_service.get_mail()