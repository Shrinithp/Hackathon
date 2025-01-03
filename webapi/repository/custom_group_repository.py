from webapi.repository.model.Email_model import EmailModel
from webapi.repository.db import db
from webapi.repository.tables.dim_recipients import Recipients
from webapi.repository.tables.fact_emails import FactEmails
from flask import jsonify

class GroupService:
    def get_group_email(self, user_id, group_id):
        try:
            # Validate and handle group_id
            if group_id == 'all':
                email_entries = db.session.query(FactEmails).filter(
                    FactEmails.userid == user_id,
                    FactEmails.is_deleted == False
                ).all()
            else:
                try:
                    group_id = int(group_id)
                except ValueError:
                    return jsonify({"error": "Invalid group_id"}), 400  # Bad Request

                email_entries = db.session.query(FactEmails).filter(
                    FactEmails.userid == user_id,
                    FactEmails.group_id == group_id,
                    FactEmails.is_deleted == False
                ).all()

            if not email_entries:
                return jsonify([])  # Return an empty list if no emails are found

            email_models = []

            for email_entry in email_entries:
                # Fetch recipients for the current email entry
                recipients = db.session.query(Recipients).filter(
                    Recipients.email_id == email_entry.id
                ).all()

                # Prepare recipient lists
                to_recipients = [
                    {"emailAddress": {"address": recipient.email_address}}
                    for recipient in recipients if recipient.recipient_type == 'TO'
                ]
                cc_recipients = [
                    {"emailAddress": {"address": recipient.email_address}}
                    for recipient in recipients if recipient.recipient_type == 'CC'
                ]

                # Prepare email data with sender and sentDateTime
                email_data = {
                    "subject": email_entry.subject,
                    "body": {
                        "contentType": "Text",
                        "content": email_entry.description or "",
                    },
                    "toRecipients": to_recipients,
                    "ccRecipients": cc_recipients,
                    "attachments": [],  # Add attachments logic if needed
                    "sender": {
                        "emailAddress": {
                            "address": email_entry.sender  # Use sender from FactEmails
                        }
                    },
                    "sentDateTime": email_entry.received_time.isoformat() if email_entry.received_time else None,  # Use received_time as sentDateTime
                }

                # Create EmailModel instance and add it to the list
                email_model = EmailModel(message=email_data)
                email_models.append(email_model.to_dict())

            # Return the list of emails as a JSON response
            return jsonify(email_models)

        except ValueError as ve:
            return jsonify({"error": f"Value error: {str(ve)}"}), 400  # Handle bad input
        except Exception as e:
            # Log the exception (e.g., using a logging framework)
            return jsonify({"error": "An unexpected error occurred"}), 500

        
    def sync_mail(self, user_id, email_data):
        try:
            # Step 3: Loop through the fetched emails and store them in the database
            # for email in email_data.get('value', []):
            #     subject = email.get('subject')
            #     body_content = email.get('body', {}).get('content')
            #     received_time = email.get('receivedDateTime')
            #     sender = email.get('sender', {}).get('emailAddress', {}).get('address')
            #     is_read = email.get('isRead', False)
            #     is_deleted = email.get('isDeleted', False)

            #     # Insert email record into FactEmails table
            #     new_email = FactEmails(
            #         subject=subject,
            #         body=body_content,
            #         description='',  # Set description based on actual data
            #         received_time=received_time,
            #         sender=sender,
            #         is_deleted=is_deleted,  # Adjust based on actual data
            #         is_read=is_read,  # Adjust based on actual data
            #         status="received" if not is_deleted else "deleted",  # Set status based on deletion status
            #         userid=user_id,  # Add the user_id here
            #         group_id=1  # Add the group_id here (could come from email or context)
            #     )

            #     db.session.add(new_email)
            #     db.session.commit()  # Commit the new email record

            #     # Step 4: Insert recipients into Recipients table
            #     # Handle TO recipients
            #     to_recipients = email.get("toRecipients", [])
            #     for recipient in to_recipients:
            #         email_address = recipient.get("emailAddress", {}).get("address")
            #         recipient_type = "TO"  # All toRecipients are TO

            #         new_recipient = Recipients(
            #             email_id=new_email.id,
            #             recipient_type=recipient_type,
            #             email_address=email_address,
            #         )

            #         db.session.add(new_recipient)

            #     # Handle CC recipients
            #     cc_recipients = email.get("ccRecipients", [])
            #     for recipient in cc_recipients:
            #         email_address = recipient.get("emailAddress", {}).get("address")
            #         recipient_type = "CC"  # All ccRecipients are CC

            #         new_recipient = Recipients(
            #             email_id=new_email.id,
            #             recipient_type=recipient_type,
            #             email_address=email_address,
            #         )

            #         db.session.add(new_recipient)

            #     # Handle BCC recipients
            #     bcc_recipients = email.get("bccRecipients", [])
            #     for recipient in bcc_recipients:
            #         email_address = recipient.get("emailAddress", {}).get("address")
            #         recipient_type = "BCC"  # All bccRecipients are BCC

            #         new_recipient = Recipients(
            #             email_id=new_email.id,
            #             recipient_type=recipient_type,
            #             email_address=email_address,
            #         )

            #         db.session.add(new_recipient)

            #     db.session.commit()  # Commit the recipients after insertion

            all_emails = db.session.query(FactEmails).filter(
                FactEmails.userid == user_id
            ).all()

            all_emails_dictionary =[]
            for email in all_emails:
                all_emails_dictionary.append(email.to_dict())

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            # Log or handle the error as needed
            print(f"Error syncing email data: {e}")
        
        # You can return any necessary data if required, or just return the email_data
        return all_emails_dictionary

