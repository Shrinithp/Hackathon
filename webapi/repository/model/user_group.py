from webapi.repository.db import db  
from datetime import datetime
from sqlalchemy.sql import func

class UserGroupMap(db.Model):
    __tablename__ = 'user_group_map'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('dim_group.group_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    # Relationship to DimGroup (optional)
    group = db.relationship('DimGroup', backref=db.backref('user_group_maps', lazy=True))

    def __repr__(self):
        return f"<UserGroupMap user_id={self.user_id} group_id={self.group_id}>"
