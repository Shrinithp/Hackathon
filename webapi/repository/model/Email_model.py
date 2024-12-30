# email_model.py
class EmailAddress:
    def __init__(self, address):
        self.address = address


class Recipient:
    def __init__(self, emailAddress):
        self.emailAddress = EmailAddress(**emailAddress)


class Body:
    def __init__(self, contentType, content):
        self.contentType = contentType
        self.content = content


class Attachment:
    def __init__(self, name, contentBytes, contentType):
        self.name = name
        self.contentBytes = contentBytes  # Base64-encoded content
        self.contentType = contentType


class Message:
    def __init__(self, subject, body, toRecipients, ccRecipients=None, attachments=None):
        self.subject = subject
        self.body = Body(**body)
        self.toRecipients = [Recipient(**recipient) for recipient in toRecipients]
        self.ccRecipients = [Recipient(**recipient) for recipient in ccRecipients] if ccRecipients else []
        self.attachments = [Attachment(**attachment) for attachment in attachments] if attachments else []


class EmailModel:
    def __init__(self, message, saveToSentItems="false"):
        self.message = Message(**message)
        self.saveToSentItems = saveToSentItems

    @staticmethod
    def from_dict(data):
        """
        Converts a dictionary (parsed from JSON) into an EmailModel instance.
        """
        return EmailModel(**data)

    def to_dict(self):
        """
        Converts the EmailModel instance back into a dictionary.
        """
        return {
            "message": {
                "subject": self.message.subject,
                "body": {
                    "contentType": self.message.body.contentType,
                    "content": self.message.body.content,
                },
                "toRecipients": [
                    {"emailAddress": {"address": recipient.emailAddress.address}}
                    for recipient in self.message.toRecipients
                ],
                "ccRecipients": [
                    {"emailAddress": {"address": recipient.emailAddress.address}}
                    for recipient in self.message.ccRecipients
                ],
                "attachments": [
                    {
                        "name": attachment.name,
                        "contentBytes": attachment.contentBytes,
                        "contentType": attachment.contentType,
                    }
                    for attachment in self.message.attachments
                ],
            },
            "saveToSentItems": self.saveToSentItems,
        }
