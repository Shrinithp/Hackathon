from webapi.repository.db import db  
from sqlalchemy.sql import func

class DimGroup(db.Model):
    __tablename__ = 'dim_group'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), unique=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=False)  # New column for default group status
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
