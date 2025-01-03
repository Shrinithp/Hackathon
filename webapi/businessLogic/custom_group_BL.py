from flask import Flask, jsonify, request, redirect
from webapi.businessLogic.inital_mail_grouper import MailGrouper
from webapi.businessLogic.response_email import MailResponder
from webapi.businessLogic.summary_email import MailSummarizer
from webapi.repository.custom_group_repository import GroupService

class GroupBL:
    def get_group_email(user_id, group_id):
        group_service = GroupService()
        return group_service.get_group_email(user_id, group_id)
    
    def sync_mail(user_id, response):
        group_service = GroupService()
        all_mails = group_service.sync_mail(user_id, response)
        # mail_grouper = MailGrouper(all_mails)
        # output = mail_grouper.run()
        # responder = MailResponder()
        # reply = responder.generate_reply('Hi Team, The client has asked for a detailed timeline for the data migration project. They’re expecting the document by tomorrow EOD. I’ll need inputs from everyone involved in this project to finalize the details. Please send me your updates ASAP. Thanks, Rahul Chawla')

        summarizer = MailSummarizer()
        summary = summarizer.summarize('Hi Team, The client has asked for a detailed timeline for the data migration project. They’re expecting the document by tomorrow EOD. I’ll need inputs from everyone involved in this project to finalize the details. Please send me your updates ASAP. Thanks, Rahul Chawla')
        return all_mails
    
    def get_mail_response(mail_body):
        mail_responder = MailResponder()
        return mail_responder.generate_reply(mail_body)
    
    def get_email_summary(mail_body):
        summarizer = MailSummarizer()
        return summarizer.summarize(mail_body)