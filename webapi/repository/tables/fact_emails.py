from webapi.repository.db import db
from sqlalchemy.sql import func

class FactEmails(db.Model):
    __tablename__ = 'fact_emails'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    description = db.Column(db.Text)
    received_time = db.Column(db.DateTime, default=func.current_timestamp())
    sender = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey('dim_group.group_id', ondelete='SET NULL'))
    is_read = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='unprocessed')
    userid = db.Column(db.String(50), nullable=False)  # Updated to varchar(50)

    group = db.relationship('DimGroup', backref=db.backref('fact_emails', lazy=True))

    def __repr__(self):
        return f'<FactEmails {self.id} - {self.subject}>'
