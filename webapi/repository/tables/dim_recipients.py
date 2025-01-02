from webapi.repository.db import db

class Recipients(db.Model):
    __tablename__ = 'dim_recipients'

    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey('fact_emails.id', ondelete='CASCADE'))
    recipient_type = db.Column(db.String(10), nullable=False)
    email_address = db.Column(db.String(255))

    email = db.relationship('FactEmails', backref=db.backref('recipients', lazy=True))

    def __repr__(self):
        return f'<Recipients {self.id} - {self.email_address}>'
